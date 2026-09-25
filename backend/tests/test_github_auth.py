from pathlib import Path

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from backend.app.services.github.auth import GitHubAppAuthenticator


APP_ID = 5069705


def generate_test_private_key() -> str:
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")


def test_create_jwt(tmp_path: Path) -> None:
    private_key = generate_test_private_key()

    private_key_path = tmp_path / "private-key.pem"
    private_key_path.write_text(private_key)

    authenticator = GitHubAppAuthenticator(
        app_id=APP_ID,
        private_key_path=str(private_key_path),
    )

    token = authenticator.create_jwt()

    payload = jwt.decode(
        token,
        options={"verify_signature": False},
    )

    assert payload["iss"] == str(APP_ID)
    assert "iat" in payload
    assert "exp" in payload