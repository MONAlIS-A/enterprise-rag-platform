from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.entities.document import (
    Document,
    DocumentSourceType,
    DocumentStatus,
)
from app.domain.repositories.document_repository import DocumentRepository


class CreateDocumentUseCase:
    def __init__(self, document_repository: DocumentRepository) -> None:
        self.document_repository = document_repository

    def execute(
        self,
        title: str,
        source_type: DocumentSourceType,
        source_uri: str,
        owner_id: UUID,
    ) -> Document:
        now = datetime.now(timezone.utc)

        document = Document(
            id=uuid4(),
            title=title,
            source_type=source_type,
            source_uri=source_uri,
            status=DocumentStatus.PENDING,
            owner_id=owner_id,
            created_at=now,
            updated_at=now,
        )

        return self.document_repository.save(document)