.PHONY: apply-bootstrap validate-bootstrap \
        install-cert-manager apply-cert-manager validate-cert-manager export-ca-for-vault \
        install-cnpg apply-cnpg validate-cnpg \
        clean

KUBECTL ?= kubectl
HELM ?= helm
KUSTOMIZE ?= kustomize

bootstrap/00-namespaces.yaml \
bootstrap/01-network-policies.yaml \
bootstrap/02-rbac-bootstrap.yaml: ;

platform/cert-manager/00-selfsign-bootstrap.yaml \
platform/cert-manager/01-internal-ca.yaml \
platform/cert-manager/02-pod-client-cert-issuers.yaml: ;

apply-bootstrap: validate-bootstrap
	$(KUBECTL) apply -f bootstrap/00-namespaces.yaml
	$(KUBECTL) apply -f bootstrap/01-network-policies.yaml
	$(KUBECTL) apply -f bootstrap/02-rbac-bootstrap.yaml

validate-bootstrap:
	@for f in bootstrap/00-namespaces.yaml bootstrap/01-network-policies.yaml bootstrap/02-rbac-bootstrap.yaml; do \
	  $(KUBECTL) apply --dry-run=client -f $$f >/dev/null || { echo "validation failed for $$f"; exit 1; }; \
	done
	@echo "bootstrap manifests validated"

install-cert-manager:
	./scripts/install-cert-manager.sh

apply-cert-manager: validate-cert-manager
	$(KUBECTL) apply -f platform/cert-manager/00-selfsign-bootstrap.yaml
	$(KUBECTL) apply -f platform/cert-manager/01-internal-ca.yaml
	$(KUBECTL) apply -f platform/cert-manager/02-pod-client-cert-issuers.yaml
	@echo "waiting for internal-ca Certificate to be Ready"
	$(KUBECTL) wait --namespace cert-manager --for=condition=Ready certificate/internal-ca --timeout=120s
	@echo "internal CA ready"

validate-cert-manager:
	@for f in platform/cert-manager/00-selfsign-bootstrap.yaml platform/cert-manager/01-internal-ca.yaml platform/cert-manager/02-pod-client-cert-issuers.yaml; do \
	  $(KUBECTL) apply --dry-run=client -f $$f >/dev/null || { echo "validation failed for $$f"; exit 1; }; \
	done
	@echo "cert-manager manifests validated"

export-ca-for-vault:
	./scripts/export-ca-for-vault.sh

install-cnpg:
	./scripts/install-cnpg.sh

apply-cnpg: validate-cnpg
	$(KUBECTL) apply -f platform/cloudnative-pg/03-db-credentials.yaml
	$(KUBECTL) apply -f platform/cloudnative-pg/00-vault-db.yaml
	$(KUBECTL) apply -f platform/cloudnative-pg/01-polaris-db.yaml
	$(KUBECTL) apply -f platform/cloudnative-pg/02-lldap-db.yaml
	@echo "waiting for CNPG clusters to be Ready"
	$(KUBECTL) wait --namespace postgres --for=condition=Ready cluster/vault-db --timeout=300s
	$(KUBECTL) wait --namespace postgres --for=condition=Ready cluster/polaris-db --timeout=300s
	$(KUBECTL) wait --namespace postgres --for=condition=Ready cluster/lldap-db --timeout=300s
	@echo "CNPG clusters ready"

validate-cnpg:
	@for f in platform/cloudnative-pg/00-vault-db.yaml platform/cloudnative-pg/01-polaris-db.yaml platform/cloudnative-pg/02-lldap-db.yaml platform/cloudnative-pg/03-db-credentials.yaml; do \
	  $(KUBECTL) apply --dry-run=client -f $$f >/dev/null || { echo "validation failed for $$f"; exit 1; }; \
	done
	@echo "cloudnative-pg manifests validated"

clean:
	$(KUBECTL) delete -f platform/cert-manager/02-pod-client-cert-issuers.yaml --ignore-not-found
	$(KUBECTL) delete -f platform/cert-manager/01-internal-ca.yaml --ignore-not-found
	$(KUBECTL) delete -f platform/cert-manager/00-selfsign-bootstrap.yaml --ignore-not-found
	$(KUBECTL) delete -f bootstrap/02-rbac-bootstrap.yaml --ignore-not-found
	$(KUBECTL) delete -f bootstrap/01-network-policies.yaml --ignore-not-found
	$(KUBECTL) delete -f bootstrap/00-namespaces.yaml --ignore-not-found
	$(KUBECTL) delete -f platform/cloudnative-pg/02-lldap-db.yaml --ignore-not-found
	$(KUBECTL) delete -f platform/cloudnative-pg/01-polaris-db.yaml --ignore-not-found
	$(KUBECTL) delete -f platform/cloudnative-pg/00-vault-db.yaml --ignore-not-found
	$(KUBECTL) delete -f platform/cloudnative-pg/03-db-credentials.yaml --ignore-not-found
