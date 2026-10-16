#! /bin/bash

k3d registry \
    create ice-registry.localhost \
    --port 12000


k3d cluster \
    create ice \
    --registry-use k3d-ice-registry.localhost:12000 \
    --agents 1 \
    -p "32000-32010:32000-32010@server:0"


k3d kubeconfig get ice > $HOME/.kube/config