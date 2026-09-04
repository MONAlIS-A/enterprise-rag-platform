from datetime import datetime, timezone
from unittest.mock import Mock
from uuid import uuid4

import pytest

from app.application.use_cases.start_document_processing import (
    StartDocumentProcessingUseCase,
)
from app.core.exceptions import NotFoundError
from app.domain.entities.document import (
    Document,
    DocumentSourceType,
    DocumentStatus,
)
from app.domain.repositories.document_repository import DocumentRepository


def create_test_document(
    status: DocumentStatus = DocumentStatus.PENDING,
) -> Document:
    now = datetime.now(timezone.utc)

    return Document(
        id=uuid4(),
        title="Test Document",
        source_type=DocumentSourceType.TEXT,
        source_uri="test://document",
        status=status,
        owner_id=uuid4(),
        created_at=now,
        updated_at=now,
    )


def test_start_processing_transitions_pending_to_processing():
    document = create_test_document()

    repository = Mock(spec=DocumentRepository)
    repository.get_by_id.return_value = document
    repository.save.return_value = document

    use_case = StartDocumentProcessingUseCase(repository)

    result = use_case.execute(document.id)

    assert result.status == DocumentStatus.PROCESSING
    assert document.status == DocumentStatus.PROCESSING

    repository.get_by_id.assert_called_once_with(document.id)
    repository.save.assert_called_once_with(document)


def test_start_processing_raises_not_found_when_document_is_missing():
    document_id = uuid4()

    repository = Mock(spec=DocumentRepository)
    repository.get_by_id.return_value = None

    use_case = StartDocumentProcessingUseCase(repository)

    with pytest.raises(NotFoundError) as exc_info:
        use_case.execute(document_id)

    assert "was not found" in str(exc_info.value)

    repository.get_by_id.assert_called_once_with(document_id)
    repository.save.assert_not_called()


def test_start_processing_rejects_invalid_state_transition():
    document = create_test_document(status=DocumentStatus.READY)

    repository = Mock(spec=DocumentRepository)
    repository.get_by_id.return_value = document

    use_case = StartDocumentProcessingUseCase(repository)

    with pytest.raises(ValueError) as exc_info:
        use_case.execute(document.id)

    assert "Invalid document status transition" in str(exc_info.value)

    repository.get_by_id.assert_called_once_with(document.id)
    repository.save.assert_not_called()