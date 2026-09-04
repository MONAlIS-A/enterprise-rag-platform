from uuid import UUID

from app.core.exceptions import NotFoundError
from app.domain.entities.document import Document, DocumentStatus
from app.domain.repositories.document_repository import DocumentRepository


class StartDocumentProcessingUseCase:
    def __init__(self, document_repository: DocumentRepository) -> None:
        self.document_repository = document_repository

    def execute(self, document_id: UUID) -> Document:
        document = self.document_repository.get_by_id(document_id)

        if document is None:
            raise NotFoundError(
                f"Document with id '{document_id}' was not found."
            )

        document.transition_to(DocumentStatus.PROCESSING)

        return self.document_repository.save(document)