from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.domain.entities.document import DocumentSourceType


class ErrorDetail(BaseModel):
    code: str = Field(..., description="Machine-readable error code.")
    message: str = Field(..., description="Human-readable error message.")


class ErrorResponse(BaseModel):
    error: ErrorDetail


class CreateDocumentRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    source_type: DocumentSourceType
    source_uri: str = Field(..., min_length=1, max_length=2048)
    owner_id: UUID


class DocumentResponse(BaseModel):
    id: UUID
    title: str
    source_type: DocumentSourceType
    source_uri: str
    status: str
    owner_id: UUID
    created_at: datetime
    updated_at: datetime