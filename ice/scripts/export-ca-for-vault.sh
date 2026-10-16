#!/usr/bin/env bash
set -euo pipefail

: "${KUBECTL:=kubectl}"
: "${SOPS_AGE_RECIPIENT_FILE:=}"
: "${VAULT_CA_SECRET_NAME:=internal-ca}"
: "${VAULT_CA_SECRET_NAMESPACE:=cert-manager}"

echo ">>> extracting CA certificate from Secret ${VAULT_CA_SECRET_NAMESPACE}/${VAULT_CA_SECRET_NAME}"
CA_FILE=$(mktemp)
trap 'rm -f "${CA_FILE}"' EXIT
${KUBECTL} get secret -n "${VAULT_CA_SECRET_NAMESPACE}" "${VAULT_CA_SECRET_NAME}" \
  -o jsonpath='{.data.tls\.crt}' | base64 -d > "${CA_FILE}"

echo ">>> CA bundle written to ${CA_FILE}"
echo "    hand to Vault via:"
echo "    vault write auth/cert/certs/<sa-name> certificate=@${CA_FILE}"
echo "    (or use scripts/bootstrap-vault.sh to register all per-namespace SAs)"
