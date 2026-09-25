import time
from pathlib import Path

import jwt


class GitHubAppAuthenticator:
    def __init__(
        self,
        app_id: int,
        private_key_path: str,
    ) -> None:
        self.app_id = app_id
        self.private_key_path = Path(private_key_path)

    def create_jwt(self) -> str:
        private_key = self.private_key_path.read_text()

        now = int(time.time())

        payload = {
            "iat": now - 60,
            "exp": now + (10 * 60),
            "iss": str(self.app_id),
        }

        return jwt.encode(
            payload,
            private_key,
            algorithm="RS256",
        )
