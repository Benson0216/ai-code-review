from fastapi import APIRouter, HTTPException, Request

from backend.app.config import settings
from backend.app.services.github.signature import verify_signature

router = APIRouter()


@router.post("/webhooks/github")
async def github_webhook(request: Request) -> dict[str, str]:
    payload = await request.body()

    signature = request.headers.get(
        "X-Hub-Signature-256",
        "",
    )

    if not verify_signature(
        payload,
        signature,
        settings.github_webhook_secret,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid webhook signature",
        )

    data = await request.json()

    action = data.get("action", "unknown")

    return {
        "status": "received",
        "action": action,
    }