from datetime import datetime, timezone
from uuid import uuid4

from app.application.dto.create_document import CreateDocumentCommand
from app.domain.entities.document import Document, DocumentStatus
from app.domain.repositories.document_repository import DocumentRepository


class CreateDocumentUseCase:
    def __init__(self, document_repository: DocumentRepository) -> None:
        self.document_repository = document_repository

    def execute(self, command: CreateDocumentCommand) -> Document:
        now = datetime.now(timezone.utc)

        document = Document(
            id=uuid4(),
            title=command.title,
            source_type=command.source_type,
            source_uri=command.source_uri,
            status=DocumentStatus.PENDING,
            owner_id=command.owner_id,
            created_at=now,
            updated_at=now,
        )

        return self.document_repository.save(document)