from fastapi import FastAPI

from backend.app.api.github_webhook import router as github_router


app = FastAPI(
    title="AI Code Review Assistant",
    version="0.1.0",
)

app.include_router(github_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}