# Custom Polaris build: OIDC identity + Polaris-managed roles

This directory contains a minimal downstream build of Apache Polaris that enables the
authentication model described below:

- **Dex provides identity only** — it proves *who* the user is.
- **Polaris owns roles** — principal roles are granted in Polaris (via `quick-start.yaml`),
  not in Dex.
- On login, the custom `PrincipalRolesMapper` returns the pseudo-role
  `PRINCIPAL_ROLE:ALL`, which tells Polaris to activate **every** role the principal has
  been granted. No role names are duplicated in Dex.

## Files

| File | Purpose |
|---|---|
| `src/main/java/org/example/polaris/DelegatingPrincipalRolesMapper.java` | The custom `PrincipalRolesMapper` CDI bean (`@Identifier("delegate-all")`). Always returns `PRINCIPAL_ROLE:ALL`. |
| `src/main/resources/application.properties` | Downstream `application.properties`; selects `principal-roles-mapper.type=delegate-all` and maps the principal by `name`. |
| `build.gradle` | Gradle project: Java 21 + Quarkus 3.39.3 + `polaris-runtime-service:1.8.0`. |
| `Dockerfile` | Two-stage build producing a runnable Quarkus image. |

## Build the image

Run from the `ice-docker-compose` directory:

```bash
docker build -f polaris-ext/Dockerfile -t polaris-oidc-all-roles:1.8.0 .
```

## Use it in `compose.yaml`

Change the `polaris` service image from `apache/polaris:1.8.0` to the custom image, or
override it with a compose override file:

```yaml
services:
  polaris:
    image: polaris-oidc-all-roles:1.8.0
    # keep the existing volumes, environment, ports, etc.
```

Because the downstream build ships its own `application.properties` (in the runner jar),
you may either rely on that file or keep mounting your own override at
`/deployment/config/application.properties` (honored via `quarkus.config.locations`).

> ⚠️ If you keep the existing `compose.yaml` mount of
> `configuration/polaris/application.properties`, that file is treated as a **complete**
> override, so it must itself contain the two lines below — otherwise the stock
> `identity`-claim and default role mapper will be used again and external auth will fail:

```properties
polaris.oidc.principal-roles-mapper.type=delegate-all
polaris.oidc.principal-mapper.name-claim-path=name
```

## Required companion changes

1. **`quick-start.yaml`** — human users authenticated via Dex must be `type: user`, not
   `type: service`:

   ```yaml
   principals:
     judas:
       type: user
       roles:
         - service_admin
   ```

   (Leave true service accounts, e.g. `flink_npe`, as `type: service` — they authenticate
   with client secrets, not Dex.)

2. **`dex/config.yaml`** — `groups` are no longer used for Polaris role assignment; keep
   them for Trino's authorization, which reads `groups` independently.