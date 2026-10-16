#!/bin/bash
set -ex

# delete the development cluster

CLUSTER_NAME=ice
REGISTRY_NAME=ice-registry.localhost

k3d registry delete $REGISTRY_NAME
k3d cluster delete $CLUSTER_NAME
