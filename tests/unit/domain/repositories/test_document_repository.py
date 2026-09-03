from datetime import datetime, timezone
from uuid import UUID, uuid4

import pytest

from app.domain.entities.document import (
    Document,
    DocumentSourceType,
    DocumentStatus,
)
from app.domain.repositories.document_repository import DocumentRepository


class FakeDocumentRepository(DocumentRepository):
    def __init__(self) -> None:
        self.documents: dict[UUID, Document] = {}

    def save(self, document: Document) -> Document:
        self.documents[document.id] = document
        return document

    def get_by_id(self, document_id: UUID) -> Document | None:
        return self.documents.get(document_id)


def test_repository_contract_requires_save_and_get_by_id():
    with pytest.raises(TypeError):
        DocumentRepository()


def test_fake_repository_implements_contract():
    repository = FakeDocumentRepository()

    now = datetime.now(timezone.utc)
    document_id = uuid4()

    document = Document(
        id=document_id,
        title="Employee Handbook",
        source_type=DocumentSourceType.PDF,
        source_uri="documents/employee-handbook.pdf",
        status=DocumentStatus.PENDING,
        owner_id=uuid4(),
        created_at=now,
        updated_at=now,
    )

    saved_document = repository.save(document)

    assert saved_document == document
    assert repository.get_by_id(document_id) == document


def test_repository_returns_none_for_unknown_document():
    repository = FakeDocumentRepository()

    result = repository.get_by_id(uuid4())

    assert result is None