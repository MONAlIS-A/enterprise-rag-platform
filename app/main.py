import logging

from fastapi import FastAPI

from app.api.routes import router
from app.core.config import get_settings
from app.core.exception_handler import app_exception_handler
from app.core.exceptions import AppException
from app.core.logging import log_requests, setup_logging

setup_logging()

settings = get_settings()

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

app.middleware("http")(log_requests)

app.add_exception_handler(AppException, app_exception_handler)

app.include_router(router)

logger.info(
    "Application initialized | environment=%s",
    settings.app_env,
)
