import hashlib
import hmac
import json

from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)

WEBHOOK_SECRET = "dev-webhook-secret"


def create_signature(payload: bytes, secret: str) -> str:
    signature = hmac.new(
        secret.encode("utf-8"),
        payload,
        hashlib.sha256,
    ).hexdigest()

    return f"sha256={signature}"


def test_github_webhook_receives_event() -> None:
    payload = {
        "action": "opened",
    }

    payload_bytes = json.dumps(payload).encode("utf-8")

    signature = create_signature(
        payload_bytes,
        WEBHOOK_SECRET,
    )

    response = client.post(
        "/webhooks/github",
        content=payload_bytes,
        headers={
            "Content-Type": "application/json",
            "X-Hub-Signature-256": signature,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": "received",
        "action": "opened",
    }


def test_github_webhook_rejects_invalid_signature() -> None:
    payload = {
        "action": "opened",
    }

    response = client.post(
        "/webhooks/github",
        json=payload,
        headers={
            "X-Hub-Signature-256": "sha256=invalid",
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid webhook signature",
    }