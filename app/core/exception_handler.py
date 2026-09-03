import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from app.api.schemas import ErrorResponse
from app.core.exceptions import AppException

logger = logging.getLogger("app.exception")


async def app_exception_handler(
    request: Request,
    exc: AppException,
) -> JSONResponse:
    logger.warning(
        "%s %s | code=%s | status=%s | message=%s",
        request.method,
        request.url.path,
        exc.code,
        exc.status_code,
        exc.message,
    )

    response = ErrorResponse(
        error={
            "code": exc.code,
            "message": exc.message,
        }
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump(),
    )
