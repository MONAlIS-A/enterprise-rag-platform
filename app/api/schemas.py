from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    code: str = Field(..., description="Machine-readable error code.")
    message: str = Field(..., description="Human-readable error message.")


class ErrorResponse(BaseModel):
    error: ErrorDetail
