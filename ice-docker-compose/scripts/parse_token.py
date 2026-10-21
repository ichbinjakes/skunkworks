import base64
import json
import sys


def main():
    # Read the token from standard input (stdin) and strip any whitespace/newlines
    token = sys.stdin.read().strip()
    print("TOKEN:", token)

    if not token:
        print("Error: No token received on stdin.", file=sys.stderr)
        sys.exit(1)

    token = json.loads(token)

    access_token = token.get("access_token")
    decode_access_token(access_token)

    id_token = token.get("id_token")
    decode_id_token(id_token)


def decode_access_token(token: str):
    # Split the token into header, payload, and signature
    parts = token.split(".")
    if len(parts) != 3:
        print(
            "Error: Invalid JWT token format (expected 3 parts separated by dots).",
            file=sys.stderr,
        )
        sys.exit(1)

    payload_b64 = parts[1]

    # Fix base64url padding
    rem = len(payload_b64) % 4
    if rem > 0:
        payload_b64 += "=" * (4 - rem)

    try:
        # Decode and parse JSON
        payload_bytes = base64.urlsafe_b64decode(payload_b64)
        payload = json.loads(payload_bytes)

        # Pretty-print the resulting dictionary
        print("\nAccess Token:")
        print(json.dumps(payload, indent=2))

    except Exception as e:
        print(f"Error decoding payload: {e}", file=sys.stderr)
        sys.exit(1)


def decode_id_token(token: str):
    # 1. Split the token into Header, Payload, and Signature
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid JWT token format")

    payload_b64 = parts[1]

    # 2. Fix base64 padding (Base64url strips trailing '=')
    rem = len(payload_b64) % 4
    if rem > 0:
        payload_b64 += "=" * (4 - rem)

    try:
        # 3. Decode base64url string to bytes, then to string, and parse JSON
        payload_bytes = base64.urlsafe_b64decode(payload_b64)
        decoded_claims = json.loads(payload_bytes.decode("utf-8"))

        # Print your Dex claims (sub, email, groups, etc.)
        print("\nID Token:")
        print(json.dumps(decoded_claims, indent=2))

    except Exception as e:
        print(f"Failed to decode token: {e}")


if __name__ == "__main__":
    main()
