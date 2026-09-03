from app.domain.entities.document import Document, DocumentSourceType, DocumentStatus
from app.infrastructure.database.models.document import DocumentModel


def to_model(document: Document) -> DocumentModel:
    return DocumentModel(
        id=document.id,
        title=document.title,
        source_type=document.source_type.value,
        source_uri=document.source_uri,
        status=document.status.value,
        owner_id=document.owner_id,
        created_at=document.created_at,
        updated_at=document.updated_at,
    )


def to_entity(model: DocumentModel) -> Document:
    return Document(
        id=model.id,
        title=model.title,
        source_type=DocumentSourceType(model.source_type),
        source_uri=model.source_uri,
        status=DocumentStatus(model.status),
        owner_id=model.owner_id,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )
