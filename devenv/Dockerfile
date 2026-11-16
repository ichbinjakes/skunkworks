# syntax=docker/dockerfile:1

FROM rockylinux:9

# --- Tool versions (bump as needed) -----------------------------------------
ARG KUBECTL_VERSION=v1.37.2
ARG HELM_VERSION=v4.3.2
ARG JQ_VERSION=jq-1.8.2
ARG EZA_VERSION=v0.23.5
ARG HELIX_VERSION=25.07.1
ARG STARSHIP_VERSION=v1.27.0
ARG ZELLIJ_VERSION=v0.46.0
ARG FD_VERSION=v10.5.2
ARG JUST_VERSION=1.59.0
ARG DELTA_VERSION=0.20.1
ARG BAT_VERSION=v0.26.1
ARG RG_VERSION=15.2.0
ARG K9S_VERSION=v0.51.0
ARG MACCHINA_VERSION=v6.4.0
ARG TUICR_VERSION=v0.28.0

# --- UID/GID of the in-container user (match your host user) ----------------
ARG UID=1000
ARG GID=1000

LABEL org.opencontainers.image.title="devbox" \
      org.opencontainers.image.description="Rocky Linux 9 development container with modern CLI tools" \
      org.opencontainers.image.base.name="docker.io/library/rockylinux:9"

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    EDITOR=hx \
    VISUAL=hx \
    BAT_THEME=TwoDark \
    HELIX_RUNTIME=/usr/lib/helix/runtime

# --- Base packages ----------------------------------------------------------
# (the base image already ships curl-minimal, which provides `curl`)
RUN dnf install -y --setopt=install_weak_deps=False --setopt=tsflags=nodocs \
        bash-completion \
        ca-certificates \
        findutils \
        git \
        gnupg2 \
        gzip \
        hostname \
        less \
        ncurses \
        openssh-clients \
        procps-ng \
        shadow-utils \
        sudo \
        tar \
        tree \
        unzip \
        which \
        xz \
    && dnf clean all \
    && rm -rf /var/cache/dnf /var/cache/yum

# --- Prebuilt tools (Linux x86_64 / static-musl where available) -------------
RUN set -eux; \
    tmp="$(mktemp -d)"; \
    cd "${tmp}"; \
    \
    # kubectl
    curl -fsSL -o kubectl "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl"; \
    install -m 0755 kubectl /usr/local/bin/kubectl; \
    \
    # helm
    curl -fsSL -o helm.tar.gz "https://get.helm.sh/helm-${HELM_VERSION}-linux-amd64.tar.gz"; \
    tar -xzf helm.tar.gz; \
    install -m 0755 linux-amd64/helm /usr/local/bin/helm; \
    \
    # jq
    curl -fsSL -o jq "https://github.com/jqlang/jq/releases/download/${JQ_VERSION}/jq-linux-amd64"; \
    install -m 0755 jq /usr/local/bin/jq; \
    \
    # k9s
    curl -fsSL -o k9s.tar.gz "https://github.com/derailed/k9s/releases/download/${K9S_VERSION}/k9s_Linux_amd64.tar.gz"; \
    mkdir k9s; tar -xzf k9s.tar.gz -C k9s; \
    install -m 0755 k9s/k9s /usr/local/bin/k9s; \
    \
    # eza
    curl -fsSL -o eza.tar.gz "https://github.com/eza-community/eza/releases/download/${EZA_VERSION}/eza_x86_64-unknown-linux-musl.tar.gz"; \
    mkdir eza; tar -xzf eza.tar.gz -C eza; \
    install -m 0755 eza/eza /usr/local/bin/eza; \
    \
    # ripgrep
    curl -fsSL -o ripgrep.tar.gz "https://github.com/BurntSushi/ripgrep/releases/download/${RG_VERSION}/ripgrep-${RG_VERSION}-x86_64-unknown-linux-musl.tar.gz"; \
    mkdir ripgrep; tar -xzf ripgrep.tar.gz -C ripgrep; \
    install -m 0755 "ripgrep/ripgrep-${RG_VERSION}-x86_64-unknown-linux-musl/rg" /usr/local/bin/rg; \
    \
    # fd
    curl -fsSL -o fd.tar.gz "https://github.com/sharkdp/fd/releases/download/${FD_VERSION}/fd-${FD_VERSION}-x86_64-unknown-linux-musl.tar.gz"; \
    mkdir fd; tar -xzf fd.tar.gz -C fd; \
    install -m 0755 "fd/fd-${FD_VERSION}-x86_64-unknown-linux-musl/fd" /usr/local/bin/fd; \
    \
    # bat
    curl -fsSL -o bat.tar.gz "https://github.com/sharkdp/bat/releases/download/${BAT_VERSION}/bat-${BAT_VERSION}-x86_64-unknown-linux-musl.tar.gz"; \
    mkdir bat; tar -xzf bat.tar.gz -C bat; \
    install -m 0755 "bat/bat-${BAT_VERSION}-x86_64-unknown-linux-musl/bat" /usr/local/bin/bat; \
    \
    # delta
    curl -fsSL -o delta.tar.gz "https://github.com/dandavison/delta/releases/download/${DELTA_VERSION}/delta-${DELTA_VERSION}-x86_64-unknown-linux-musl.tar.gz"; \
    mkdir delta; tar -xzf delta.tar.gz -C delta; \
    install -m 0755 "delta/delta-${DELTA_VERSION}-x86_64-unknown-linux-musl/delta" /usr/local/bin/delta; \
    \
    # just
    curl -fsSL -o just.tar.gz "https://github.com/casey/just/releases/download/${JUST_VERSION}/just-${JUST_VERSION}-x86_64-unknown-linux-musl.tar.gz"; \
    mkdir just; tar -xzf just.tar.gz -C just; \
    install -m 0755 just/just /usr/local/bin/just; \
    \
    # starship
    curl -fsSL -o starship.tar.gz "https://github.com/starship/starship/releases/download/${STARSHIP_VERSION}/starship-x86_64-unknown-linux-musl.tar.gz"; \
    mkdir starship; tar -xzf starship.tar.gz -C starship; \
    install -m 0755 starship/starship /usr/local/bin/starship; \
    \
    # zellij
    curl -fsSL -o zellij.tar.gz "https://github.com/zellij-org/zellij/releases/download/${ZELLIJ_VERSION}/zellij-x86_64-unknown-linux-musl.tar.gz"; \
    mkdir zellij; tar -xzf zellij.tar.gz -C zellij; \
    install -m 0755 zellij/zellij /usr/local/bin/zellij; \
    \
    # macchina
    curl -fsSL -o macchina.tar.gz "https://github.com/Macchina-CLI/macchina/releases/download/${MACCHINA_VERSION}/macchina-${MACCHINA_VERSION}-linux-musl-x86_64.tar.gz"; \
    mkdir macchina; tar -xzf macchina.tar.gz -C macchina; \
    install -m 0755 macchina/macchina /usr/local/bin/macchina; \
    \
    # tuicr
    curl -fsSL -o tuicr.tar.gz "https://github.com/agavra/tuicr/releases/download/${TUICR_VERSION}/tuicr-${TUICR_VERSION#v}-x86_64-unknown-linux-musl.tar.gz"; \
    mkdir tuicr; tar -xzf tuicr.tar.gz -C tuicr; \
    install -m 0755 tuicr/tuicr /usr/local/bin/tuicr; \
    \
    # helix (binary + runtime, looked up via HELIX_RUNTIME)
    curl -fsSL -o helix.tar.xz "https://github.com/helix-editor/helix/releases/download/${HELIX_VERSION}/helix-${HELIX_VERSION}-x86_64-linux.tar.xz"; \
    mkdir -p /usr/lib/helix; \
    tar -xJf helix.tar.xz -C /usr/lib/helix --strip-components=1; \
    ln -sf /usr/lib/helix/hx /usr/local/bin/hx; \
    ln -sf /usr/lib/helix/hx /usr/local/bin/helix; \
    \
    # shell completions
    mkdir -p /etc/bash_completion.d; \
    kubectl completion bash > /etc/bash_completion.d/kubectl; \
    helm completion bash > /etc/bash_completion.d/helm; \
    \
    # strip debug symbols to keep the image smaller
    for bin in /usr/local/bin/*; do strip --strip-unneeded "${bin}" || true; done; \
    strip --strip-unneeded /usr/lib/helix/hx || true; \
    \
    cd /; rm -rf "${tmp}"

# --- Non-root user matching the host UID/GID --------------------------------
RUN set -eux; \
    if getent group "${GID}" >/dev/null; then \
        grp="$(getent group "${GID}" | cut -d: -f1)"; \
    else \
        groupadd -g "${GID}" dev; \
        grp=dev; \
    fi; \
    useradd -m -u "${UID}" -g "${grp}" -G wheel -s /bin/bash dev; \
    echo 'dev ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/dev; \
    chmod 0440 /etc/sudoers.d/dev; \
    mkdir -p /workspace; \
    chown -R dev:"${grp}" /home/dev /workspace

# --- Default user configuration ---------------------------------------------
RUN set -eux; \
    { \
        echo ''; \
        echo '# --- devbox ---'; \
        echo 'export EDITOR=hx'; \
        echo 'export VISUAL=hx'; \
        echo 'eval "$(starship init bash)"'; \
        echo ''; \
        echo 'alias ls="eza --icons --group-directories-first"'; \
        echo 'alias ll="eza -lah --icons --group-directories-first --git"'; \
        echo 'alias la="eza -a --icons --group-directories-first"'; \
        echo 'alias lt="eza --tree --level=2 --icons"'; \
    } >> /home/dev/.bashrc; \
    \
    printf '%s\n' \
        '[core]' \
        '    pager = delta' \
        '    editor = hx' \
        '' \
        '[interactive]' \
        '    diffFilter = delta --color-only' \
        '' \
        '[delta]' \
        '    navigate = true' \
        '    line-numbers = true' \
        '    syntax-theme = TwoDark' \
        '' \
        '[merge]' \
        '    conflictstyle = zdiff3' \
        '' \
        '[diff]' \
        '    colorMoved = default' \
        > /home/dev/.gitconfig; \
    \
    mkdir -p /home/dev/.config/helix; \
    printf '%s\n' \
        'theme = "catppuccin_mocha"' \
        '' \
        '[editor]' \
        'line-number = "relative"' \
        'mouse = true' \
        'bufferline = "multiple"' \
        '' \
        '[editor.cursor-shape]' \
        'insert = "bar"' \
        'normal = "block"' \
        > /home/dev/.config/helix/config.toml; \
    \
    chown -R dev:dev /home/dev

WORKDIR /workspace
USER dev

CMD ["/bin/bash"]
