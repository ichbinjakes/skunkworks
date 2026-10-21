# Build the custom Polaris image
# Usage: docker build -f polaris-ext/Dockerfile -t polaris-oidc-all-roles:1.8.0 .
# (run this from the ice-docker-compose directory)

# ---- Stage 1: build ----
FROM gradle:8.14-jdk21 AS build
WORKDIR /app

# Copy the build files and source.
COPY polaris-ext/settings.gradle /app/settings.gradle
COPY polaris-ext/build.gradle /app/build.gradle
COPY polaris-ext/src /app/src

# `quarkusBuild` produces the fast-jar at build/quarkus-app/ (quarkus-run.jar entry point).
RUN gradle --no-daemon quarkusBuild

# ---- Stage 2: package the Quarkus runner ----
FROM eclipse-temurin:21-jre
WORKDIR /app

# Copy the built Quarkus fast-jar directory.
COPY --from=build /app/build/quarkus-app /app/quarkus-app

# Polaris reads an optional external config here (see quarkus.config.locations).
RUN mkdir -p /deployment/config

EXPOSE 8181 8182

ENTRYPOINT ["java", "-jar", "/app/quarkus-app/quarkus-run.jar"]