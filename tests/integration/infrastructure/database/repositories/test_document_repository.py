from datetime import datetime, timezone
from uuid import uuid4

from app.domain.entities.document import (
    Document,
    DocumentSourceType,
    DocumentStatus,
)
from app.infrastructure.database.models.document import DocumentModel
from app.infrastructure.database.repositories.document_repository import (
    SqlAlchemyDocumentRepository,
)
from app.infrastructure.database.session import SessionLocal


def create_test_document() -> Document:
    now = datetime.now(timezone.utc)

    return Document(
        id=uuid4(),
        title="Integration Test Document",
        source_type=DocumentSourceType.TEXT,
        source_uri="test://integration/document",
        status=DocumentStatus.PENDING,
        owner_id=uuid4(),
        created_at=now,
        updated_at=now,
    )


def test_save_and_get_document():
    session = SessionLocal()
    document = create_test_document()

    try:
        repository = SqlAlchemyDocumentRepository(session)

        saved_document = repository.save(document)

        assert saved_document.id == document.id
        assert saved_document.title == document.title
        assert saved_document.source_type == document.source_type
        assert saved_document.status == document.status

        retrieved_document = repository.get_by_id(document.id)

        assert retrieved_document is not None
        assert retrieved_document.id == document.id
        assert retrieved_document.title == document.title
        assert retrieved_document.source_type == document.source_type
        assert retrieved_document.status == document.status

    finally:
        session.query(DocumentModel).filter(
            DocumentModel.id == document.id
        ).delete()
        session.commit()
        session.close()


def test_get_by_id_returns_none_for_unknown_document():
    session = SessionLocal()

    try:
        repository = SqlAlchemyDocumentRepository(session)

        result = repository.get_by_id(uuid4())

        assert result is None

    finally:
        session.close()