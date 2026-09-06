import hashlib
import hmac


def verify_signature(
    payload: bytes,
    signature: str,
    secret: str,
) -> bool:
    if not signature.startswith("sha256="):
        return False

    expected_signature = hmac.new(
        secret.encode("utf-8"),
        payload,
        hashlib.sha256,
    ).hexdigest()

    expected_header = f"sha256={expected_signature}"

    return hmac.compare_digest(
        signature,
        expected_header,
    )