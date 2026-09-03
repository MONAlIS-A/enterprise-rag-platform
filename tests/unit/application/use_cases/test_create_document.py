from datetime import datetime, timezone
from uuid import UUID, uuid4

import pytest

from app.application.use_cases.create_document import CreateDocumentUseCase
from app.domain.entities.document import DocumentSourceType
from app.domain.repositories.document_repository import DocumentRepository


class FakeDocumentRepository(DocumentRepository):
    def __init__(self) -> None:
        self.saved_documents = []

    def save(self, document):
        self.saved_documents.append(document)
        return document

    def get_by_id(self, document_id: UUID):
        return next(
            (
                document
                for document in self.saved_documents
                if document.id == document_id
            ),
            None,
        )


def test_create_document_creates_pending_document():
    repository = FakeDocumentRepository()
    use_case = CreateDocumentUseCase(repository)

    owner_id = uuid4()

    document = use_case.execute(
        title="Employee Handbook",
        source_type=DocumentSourceType.PDF,
        source_uri="documents/employee-handbook.pdf",
        owner_id=owner_id,
    )

    assert document.title == "Employee Handbook"
    assert document.source_type == DocumentSourceType.PDF
    assert document.source_uri == "documents/employee-handbook.pdf"
    assert document.owner_id == owner_id
    assert document.status.value == "pending"
    assert isinstance(document.id, UUID)
    assert document.created_at.tzinfo == timezone.utc
    assert document.updated_at.tzinfo == timezone.utc


def test_create_document_saves_document_to_repository():
    repository = FakeDocumentRepository()
    use_case = CreateDocumentUseCase(repository)

    document = use_case.execute(
        title="Security Policy",
        source_type=DocumentSourceType.DOCX,
        source_uri="documents/security-policy.docx",
        owner_id=uuid4(),
    )

    assert len(repository.saved_documents) == 1
    assert repository.saved_documents[0] == document


def test_create_document_propagates_domain_validation_error():
    repository = FakeDocumentRepository()
    use_case = CreateDocumentUseCase(repository)

    with pytest.raises(
        ValueError,
        match="Document title cannot be empty.",
    ):
        use_case.execute(
            title="   ",
            source_type=DocumentSourceType.PDF,
            source_uri="documents/employee-handbook.pdf",
            owner_id=uuid4(),
        )

    assert repository.saved_documents == []