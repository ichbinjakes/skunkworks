# System Architecture & Implementation Blueprint

This document specifies the target architecture, security model, and component integration for an enterprise-grade, zero-trust Apache Iceberg data platform on Kubernetes.

---

## Architecture Overview

```
                                  +-------------------------------------------+
                                  |     Identity Provider (Tiny auth + LLDAP) |
                                  +-------------------+-----------------------+
                                                      | OIDC JWT
                                                      v
+-----------------------+         +-------------------+-------------------+
| Flink / Kafka Connect |         |    Kubernetes Ingress (mTLS / TLS 1.3) |
+-----------+-----------+         +-------------------+-------------------+
            |                                         |
            | Client Cert (mTLS)                      v
            |                        +----------------+-------------------+
            v                        |           Trino Coordinator        |
+-----------+-----------+            +--------+------------------+--------+
| HashiCorp Vault       |                     |                  |
| (auth/cert Engine)    |  OPA Authz Payload  v                  v EventListener SPI
+-----------+-----------+            +--------+---------+      +-+-------------------+
            |                        | Trino OPA Plugin |      | Fluent Bit Logger   |
            | S3 Keys                +--------+---------+      +----------+----------+
            v                                 |                           |
+-----------+-----------+                     v JSON Decisions            v JSON Stream
| On-Prem S3 Storage    |<--------------------+--------------------------+ Kafka / SIEM
| (RustFS )             |  Direct S3 Reads
+-----------------------+

```

---

## Core Component Specifications

### 1. HashiCorp Vault TLS Certificate Authentication (`auth/cert`)

Replaces JWT-based Kubernetes authentication with mTLS client certificate verification via `cert-manager`.

```
[cert-manager] ──Issuers/CRDs──► [Pod TLS Secret (tls.crt / tls.key)]
                                              │
                                              │ mTLS Handshake (/v1/auth/cert/login)
                                              ▼
                                   [HashiCorp Vault Server]
                                              │
                                   Validates SAN/CN against CA
                                              │
                                              ▼
                                   Issues Vault Token with Policy

```

* **Certificate Provisioning:** `cert-manager` running in Kubernetes uses an internal CA to issue short-lived X.509 client certificates to Pods via `Certificate` CRDs.
* **Identity Format:** SANs (Subject Alternative Names) follow the convention `spiffe://cluster.local/ns/<namespace>/sa/<serviceaccount-name>` or CN `<serviceaccount-name>.<namespace>.svc`.
* **Vault Configuration:**
```bash
# Enable TLS Cert Auth
vault auth enable cert

# Register CA and bind Common Name / SAN to Vault Policy
vault write auth/cert/certs/orders-ingestion \
    display_name="orders-ingestion-sa" \
    policies="s3-sales-orders-write" \
    certificate=@/etc/vault/certs/k8s-ca.crt \
    allowed_common_names="orders-ingestion-sa.ingestion.svc" \
    ttl=3600

```


* **Vault Agent Sidecar:** Runs in the ingestion pod, initiates mTLS auth using mounted `/etc/certs/tls.crt` and `/etc/certs/tls.key`, obtains a token, and fetches S3 keys to `/vault/secrets/aws-credentials`.

---

## 2. Table-Scoped S3 Path Isolation (On-Prem / Non-STS)

Enforces strict table path boundaries without cloud AWS STS dynamic session policy capabilities.

```
+---------------------------------------------------------------------------------------+
| 1. Polaris Table Creation Event  ──► [Lakehouse K8s Operator]                         |
|                                            │                                          |
|                                            ├──► 2. Provision S3 Policy (MinIO API)    |
|                                            │                                          |
|                                            └──► 3. Register Vault Cert Role           |
+---------------------------------------------------------------------------------------+
                                             |
                                             v
+---------------------------------------------------------------------------------------+
| 4. Flink Pod (orders-ingestion-sa) ──mTLS──► [Vault] ──► S3 Keys (Path Restricted)    |
+---------------------------------------------------------------------------------------+
                                             |
                                             v
+---------------------------------------------------------------------------------------+
| 5. S3 Storage Engine Enforces Path: s3://enterprise-lakehouse/sales.db/orders/*       |
+---------------------------------------------------------------------------------------+

```

1. **Table Path Registration:** Apache Polaris assigns table location (e.g., `s3://enterprise-lakehouse/sales.db/orders/`).
2. **Automated S3 Policy Provisioning:** A Kubernetes Operator intercepting Polaris events executes against the S3 Admin API (MinIO/Ceph) to create a path-scoped IAM policy:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:PutObject", "s3:GetObject", "s3:DeleteObject", "s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::enterprise-lakehouse/sales.db/orders/*",
        "arn:aws:s3:::enterprise-lakehouse"
      ],
      "Condition": {
        "StringLike": { "s3:prefix": ["sales.db/orders/*"] }
      }
    }
  ]
}

```


3. **Automated Vault Mapping:** Operator registers a Vault `auth/cert` entry mapping the K8s ServiceAccount's SAN/CN to the newly generated S3 path policy.

---

## 3. Trino Zero-Trust & Audit Architecture

* **Authentication:** Trino Coordinator enforces OIDC JWT authentication from the IdP.
* **Authorization (Trino OPA Plugin):**
* Evaluates user identity, group claims, and requested SQL AST against OPA Rego rules.
* Dynamically injects SQL `ROW FILTER` expressions (e.g., `department = 'US_FINANCE'`) and `COLUMN MASKING` expressions into Trino's logical query planner prior to execution.


* **Audit Logging (Trino EventListener SPI):**
* Emits structured JSON events on `QueryCreated` and `QueryCompleted`.
* Captures: `user`, `userGroups`, `sourceIp`, `queryId`, `rawQuery`, `accessedTables`, `opaFiltersApplied`, `processedBytes`, and `executionTimeMs`.
* Logs stream via stdout/file to Fluent Bit sidecars, routing directly to Kafka or Elasticsearch/SIEM.



---

## 4. Polaris Catalog & Ingestion Runtime

* **Apache Polaris Catalog:** Runs on Kubernetes, backed by a PostgreSQL cluster (CloudNativePG Operator) for state storage. Handless catalog-level RBAC (`CREATE_TABLE`, `ALTER_NAMESPACE`).
* **Flink & Kafka Connect Runtime:**
* Configured with `flink-s3-fs-hadoop` or Iceberg Kafka Connect S3 writers.
* Uses `com.amazonaws.auth.PropertiesFileCredentialsProvider` pointing to `/vault/secrets/aws-credentials`.
* Vault Agent continuously refreshes this credentials file on disk before lease expiration, enabling uninterrupted streaming writes without container restarts.



---

## Implementation Deliverables Checklist for Coding Agent

```
/platform-infrastructure
├── /k8s
│   ├── /crds
│   │   └── cert-manager-issuer.yaml       # K8s CA Issuer for Pod Client Certs
│   ├── /trino
│   │   ├── deployment.yaml                # Coordinator/Worker manifests with OIDC + OPA plugin
│   │   └── configmap-event-listener.yaml  # Audit Logger SPI properties
│   ├── /polaris
│   │   └── polaris-deployment.yaml        # Polaris Catalog connected to CNPG Postgres
│   └── /vault
│       └── vault-cert-auth-config.yaml    # Vault cert auth configuration scripts
├── /operator
│   └── /s3-lakehouse-operator             # K8s Operator reconciling Polaris table events
│       ├── main.go                        # Listens to table creation events
│       ├── s3_admin_client.go             # MinIO/Ceph Admin API wrapper for policy creation
│       └── vault_client.go                # Vault auth/cert role registration logic
└── /opa
    └── policies/
        └── trino_authorization.rego       # Rego policy for RBAC, row filtering, and column masking

```