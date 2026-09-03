from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.document import Document


class DocumentRepository(ABC):
    @abstractmethod
    def save(self, document: Document) -> Document:
        """Persist a document and return the saved entity."""
        ...

    @abstractmethod
    def get_by_id(self, document_id: UUID) -> Document | None:
        """Return a document by ID, or None if it does not exist."""
        ...