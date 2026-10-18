#!/usr/bin/env bash
set -euo pipefail

: "${HELM:=helm}"
: "${CNPG_VERSION:=0.23.1}"
: "${CNPG_NAMESPACE:=cnpg-system}"

echo ">>> adding cloudnative-pg helm repo"
${HELM} repo add cnpg https://cloudnative-pg.github.io/charts --force-update >/dev/null
${HELM} repo update >/dev/null

echo ">>> installing cloudnative-pg ${CNPG_VERSION}"
${HELM} upgrade --install cnpg cnpg/cloudnative-pg \
  --namespace "${CNPG_NAMESPACE}" --create-namespace \
  --version "${CNPG_VERSION}" \
  --set installCRDs=true \
  --wait

echo ">>> waiting for cnpg-controller-manager"
kubectl wait --namespace "${CNPG_NAMESPACE}" \
  --for=condition=Ready pod \
  --selector=app.kubernetes.io/name=cloudnative-pg \
  --timeout=180s
