from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from uuid import UUID

from app.api.dependencies import get_db
from app.api.schemas import CreateDocumentRequest, DocumentResponse
from app.application.dto.create_document import CreateDocumentCommand
from app.application.use_cases.create_document import CreateDocumentUseCase
from app.core.config import get_settings
from app.domain.repositories.document_repository import DocumentRepository
from app.infrastructure.database.repositories.document_repository import (
    SqlAlchemyDocumentRepository,
)
from app.infrastructure.database.session import SessionLocal
from app.application.use_cases.get_document import GetDocumentUseCase


router = APIRouter()
settings = get_settings()


def get_document_repository(
    db: Session = Depends(get_db),
) -> DocumentRepository:
    return SqlAlchemyDocumentRepository(db)


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


@router.post(
    "/documents",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_document(
    request: CreateDocumentRequest,
    repository: DocumentRepository = Depends(get_document_repository),
) -> DocumentResponse:
    use_case = CreateDocumentUseCase(repository)

    command = CreateDocumentCommand(
        title=request.title,
        source_type=request.source_type,
        source_uri=request.source_uri,
        owner_id=request.owner_id,
    )

    document = use_case.execute(command)

    return DocumentResponse(
        id=document.id,
        title=document.title,
        source_type=document.source_type,
        source_uri=document.source_uri,
        status=document.status.value,
        owner_id=document.owner_id,
        created_at=document.created_at,
        updated_at=document.updated_at,
    )

@router.get(
    "/documents/{document_id}",
    response_model=DocumentResponse,
)
def get_document(
    document_id: UUID,
    repository: DocumentRepository = Depends(get_document_repository),
) -> DocumentResponse:
    use_case = GetDocumentUseCase(repository)

    document = use_case.execute(document_id)

    return DocumentResponse(
        id=document.id,
        title=document.title,
        source_type=document.source_type,
        source_uri=document.source_uri,
        status=document.status.value,
        owner_id=document.owner_id,
        created_at=document.created_at,
        updated_at=document.updated_at,
    )
