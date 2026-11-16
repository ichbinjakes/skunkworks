## Build command: 

```bash
docker build -t devbox:latest \
  --build-arg UID=$(id -u) \
  --build-arg GID=$(id -g) \
  .
```
Note: build args default 1000. If host UID is 1001 etc, pass.

### Podman

```bash
podman build -t devbox:latest \
  --build-arg UID="$(id -u)" \
  --build-arg GID="$(id -g)" \
  .
```
 
## Run command example:

```bash
docker run --rm -it \
  --name devbox \
  -v "$PWD:/workspace" \
  -v "$HOME/.kube:/home/dev/.kube:ro" \
  -v "$HOME/.config/helm:/home/dev/.config/helm" \
  -w /workspace \
  devbox:latest
```

### Podman

```bash
podman run --rm -it \
  --name devbox \
  --userns=keep-id \
  -v "$PWD:/workspace:Z" \
  -v "$HOME/.kube:/home/dev/.kube:Z" \
  -w /workspace \
  devbox:latest
```

 ## Podman notes:

Why --userns=keep-id matters: without it, rootless Podman maps container root to your host user and container UID 1000 to a subuid. Bind-mounted host files then appear owned by container root, so the dev user can't write to them. keep-id maps your host UID to the same UID inside the container, matching dev.

Other notes:

    SELinux hosts (Rocky/RHEL/Fedora): keep :Z on bind mounts, or use --security-opt label=disable if relabeling ~/.kube causes problems for host tools.
    Non-1000 host UID: rebuilding with --build-arg UID=$(id -u) --build-arg GID=$(id -g) is the cleanest. Alternatively use --userns=keep-id:uid=1000,gid=1000 to map your host user onto the image's UID 1000.
    sudo inside the container still works (passwordless for dev), but only grants root inside the user namespace — never host root.
    macOS/Windows: podman machine runs a Linux VM, so use the same flags; permissions inside the VM's mounted /workspace may need :U or matching UID setup depending on the mount implementation.
    If podman build complains about the # syntax=docker/dockerfile:1 line, it can be removed — nothing in the file requires BuildKit.
