#!/usr/bin/env bash
set -euo pipefail

: "${HELM:=helm}"
: "${CERT_MANAGER_VERSION:=v1.16.3}"
: "${CERT_MANAGER_NAMESPACE:=cert-manager}"

echo ">>> adding jetstack helm repo"
${HELM} repo add jetstack https://charts.jetstack.io --force-update >/dev/null
${HELM} repo update >/dev/null

echo ">>> installing cert-manager ${CERT_MANAGER_VERSION} into ${CERT_MANAGER_NAMESPACE}"
${HELM} upgrade --install cert-manager jetstack/cert-manager \
  --namespace "${CERT_MANAGER_NAMESPACE}" --create-namespace \
  --version "${CERT_MANAGER_VERSION}" \
  --set installCRDs=true \
  --set featureGates=ExperimentalGatewayAPISupport=false \
  --wait

echo ">>> waiting for cert-manager webhook"
${HELM} status cert-manager -n "${CERT_MANAGER_NAMESPACE}" >/dev/null
kubectl wait --namespace "${CERT_MANAGER_NAMESPACE}" \
  --for=condition=Ready pod \
  --selector=app.kubernetes.io/name=cert-manager \
  --timeout=180s
