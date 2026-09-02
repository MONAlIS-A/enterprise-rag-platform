from fastapi import APIRouter
from sqlalchemy import text

from app.core.config import get_settings
from app.infrastructure.database.session import SessionLocal

router = APIRouter()
settings = get_settings()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/ready")
def readiness_check():
    db = SessionLocal()

    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "ready",
            "environment": settings.app_env,
            "dependencies": {
                "database": "ok",
            },
        }

    finally:
        db.close()