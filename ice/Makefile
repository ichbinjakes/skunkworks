.PHONY: apply-bootstrap validate-bootstrap clean

KUBECTL ?= kubectl
KUSTOMIZE ?= kustomize

bootstrap/00-namespaces.yaml \
bootstrap/01-network-policies.yaml \
bootstrap/02-rbac-bootstrap.yaml: ;

apply-bootstrap: validate-bootstrap
	$(KUBECTL) apply -f bootstrap/00-namespaces.yaml
	$(KUBECTL) apply -f bootstrap/01-network-policies.yaml
	$(KUBECTL) apply -f bootstrap/02-rbac-bootstrap.yaml

validate-bootstrap:
	@for f in bootstrap/00-namespaces.yaml bootstrap/01-network-policies.yaml bootstrap/02-rbac-bootstrap.yaml; do \
	  $(KUBECTL) apply --dry-run=client -f $$f >/dev/null || { echo "validation failed for $$f"; exit 1; }; \
	done
	@echo "bootstrap manifests validated"

clean:
	$(KUBECTL) delete -f bootstrap/02-rbac-bootstrap.yaml --ignore-not-found
	$(KUBECTL) delete -f bootstrap/01-network-policies.yaml --ignore-not-found
	$(KUBECTL) delete -f bootstrap/00-namespaces.yaml --ignore-not-found
