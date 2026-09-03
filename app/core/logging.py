# app/core/logging.py

import logging
import sys
import time

from fastapi import Request

from app.core.config import get_settings


def setup_logging() -> None:
    settings = get_settings()

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        force=True,
    )


logger = logging.getLogger("app.request")


async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()

    try:
        response = await call_next(request)

    except Exception:
        duration_ms = (time.perf_counter() - start_time) * 1000

        logger.exception(
            "%s %s | status=500 | duration=%.2fms",
            request.method,
            request.url.path,
            duration_ms,
        )

        raise

    duration_ms = (time.perf_counter() - start_time) * 1000

    logger.info(
        "%s %s | status=%s | duration=%.2fms",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )

    return response
