from datetime import datetime, timezone
from unittest.mock import Mock
from uuid import uuid4

import pytest

from app.application.use_cases.get_document import GetDocumentUseCase
from app.core.exceptions import NotFoundError
from app.domain.entities.document import (
    Document,
    DocumentSourceType,
    DocumentStatus,
)
from app.domain.repositories.document_repository import DocumentRepository


def create_test_document() -> Document:
    now = datetime.now(timezone.utc)

    return Document(
        id=uuid4(),
        title="Test Document",
        source_type=DocumentSourceType.TEXT,
        source_uri="test://document",
        status=DocumentStatus.PENDING,
        owner_id=uuid4(),
        created_at=now,
        updated_at=now,
    )


def test_get_document_returns_document_when_found():
    document = create_test_document()

    repository = Mock(spec=DocumentRepository)
    repository.get_by_id.return_value = document

    use_case = GetDocumentUseCase(repository)

    result = use_case.execute(document.id)

    assert result == document
    repository.get_by_id.assert_called_once_with(document.id)


def test_get_document_raises_not_found_error_when_missing():
    document_id = uuid4()

    repository = Mock(spec=DocumentRepository)
    repository.get_by_id.return_value = None

    use_case = GetDocumentUseCase(repository)

    with pytest.raises(NotFoundError) as exc_info:
        use_case.execute(document_id)

    assert "was not found" in str(exc_info.value)
    repository.get_by_id.assert_called_once_with(document_id)