#!/usr/bin/env python3
"""Fetch an access token and an id token from Dex.

Credentials come from CLI args first, then environment variables.

    python3 get_dex_token.py --dex-host http://localhost:5556 \
        --username finance@example.com --password password

    DEX_HOST=http://localhost:5556 DEX_USERNAME=finance@example.com \
    DEX_PASSWORD=password python3 get_dex_token.py
"""

import argparse
import json
import os
from typing import Any

import requests

DEFAULT_DEX_HOST = "http://localhost:5556"
DEFAULT_CLIENT_ID = "polaris"
DEFAULT_SCOPE = "openid profile groups"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Get access and id tokens from Dex")
    parser.add_argument(
        "--dex-host",
        default=os.environ.get("DEX_HOST", DEFAULT_DEX_HOST),
        help=f"Dex base URL (env DEX_HOST, default {DEFAULT_DEX_HOST})",
    )
    parser.add_argument(
        "--username",
        default=os.environ.get("DEX_USERNAME"),
        help="user name (env DEX_USERNAME)",
    )
    parser.add_argument(
        "--password",
        default=os.environ.get("DEX_PASSWORD"),
        help="password (env DEX_PASSWORD)",
    )
    parser.add_argument(
        "--client-id",
        default=os.environ.get("DEX_CLIENT_ID", DEFAULT_CLIENT_ID),
        help=f"OAuth client id (env DEX_CLIENT_ID, default {DEFAULT_CLIENT_ID})",
    )
    parser.add_argument(
        "--scope",
        default=os.environ.get("DEX_SCOPE", DEFAULT_SCOPE),
        help=f"requested scope (env DEX_SCOPE, default '{DEFAULT_SCOPE}')",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=float(os.environ.get("DEX_TIMEOUT", "10")),
        help="request timeout in seconds (env DEX_TIMEOUT, default 10)",
    )
    return parser.parse_args()


def token_url(dex_host: str) -> str:
    return f"{dex_host.rstrip('/')}/dex/token"


def fetch_tokens(dex_host: str, username: str, password: str, client_id: str, scope: str, timeout: float) -> dict[str, Any]:
    try:
        response = requests.post(
            token_url(dex_host),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "password",
                "client_id": client_id,
                "scope": scope,
                "username": username,
                "password": password,
            },
            timeout=timeout,
        )
    except requests.RequestException as exc:
        raise SystemExit(f"error: cannot reach Dex at {token_url(dex_host)}: {exc}")

    if response.status_code != 200:
        raise SystemExit(f"error: Dex returned HTTP {response.status_code}: {response.text.strip()}")

    try:
        return response.json()
    except ValueError:
        raise SystemExit(f"error: Dex returned a non-JSON response: {response.text.strip()}")


def main() -> None:
    args = parse_args()

    missing = [name for name in ("username", "password") if not getattr(args, name)]
    if missing:
        env_names = ", ".join(f"DEX_{name.upper()}" for name in missing)
        raise SystemExit(f"error: missing required value(s) for: {', '.join(missing)} (set as args or {env_names})")

    tokens = fetch_tokens(
        dex_host=args.dex_host,
        username=args.username,
        password=args.password,
        client_id=args.client_id,
        scope=args.scope,
        timeout=args.timeout,
    )

    access_token = tokens.get("access_token")
    id_token = tokens.get("id_token")
    if not access_token or not id_token:
        raise SystemExit(f"error: response missing tokens: {json.dumps(tokens)}")

    print("\n   ACCESS_TOKEN:  ", access_token)
    print("\n   ID_TOKEN:  ", id_token)
    print()


if __name__ == "__main__":
    main()