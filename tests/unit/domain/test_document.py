from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.domain.entities.document import (
    Document,
    DocumentSourceType,
    DocumentStatus,
)


def test_document_rejects_empty_title():
    now = datetime.now(UTC)

    with pytest.raises(ValueError, match="Document title cannot be empty."):
        Document(
            id=uuid4(),
            title="   ",
            source_type=DocumentSourceType.PDF,
            source_uri="documents/employee-handbook.pdf",
            status=DocumentStatus.PENDING,
            owner_id=uuid4(),
            created_at=now,
            updated_at=now,
        )


def test_document_rejects_empty_source_uri():
    now = datetime.now(UTC)

    with pytest.raises(
        ValueError,
        match="Document source URI cannot be empty.",
    ):
        Document(
            id=uuid4(),
            title="Employee Handbook",
            source_type=DocumentSourceType.PDF,
            source_uri="   ",
            status=DocumentStatus.PENDING,
            owner_id=uuid4(),
            created_at=now,
            updated_at=now,
        )


def test_document_creation_with_valid_data():
    now = datetime.now(UTC)
    document_id = uuid4()
    owner_id = uuid4()

    document = Document(
        id=document_id,
        title="Employee Handbook",
        source_type=DocumentSourceType.PDF,
        source_uri="documents/employee-handbook.pdf",
        status=DocumentStatus.PENDING,
        owner_id=owner_id,
        created_at=now,
        updated_at=now,
    )

    assert document.id == document_id
    assert document.title == "Employee Handbook"
    assert document.source_type == DocumentSourceType.PDF
    assert document.source_uri == "documents/employee-handbook.pdf"
    assert document.status == DocumentStatus.PENDING
    assert document.owner_id == owner_id
    assert document.created_at == now
    assert document.updated_at == now


def test_document_allows_valid_status_transition():
    now = datetime.now(UTC)

    document = Document(
        id=uuid4(),
        title="Employee Handbook",
        source_type=DocumentSourceType.PDF,
        source_uri="documents/employee-handbook.pdf",
        status=DocumentStatus.PENDING,
        owner_id=uuid4(),
        created_at=now,
        updated_at=now,
    )

    document.transition_to(DocumentStatus.PROCESSING)

    assert document.status == DocumentStatus.PROCESSING


def test_document_rejects_invalid_status_transition():
    now = datetime.now(UTC)

    document = Document(
        id=uuid4(),
        title="Employee Handbook",
        source_type=DocumentSourceType.PDF,
        source_uri="documents/employee-handbook.pdf",
        status=DocumentStatus.PROCESSING,
        owner_id=uuid4(),
        created_at=now,
        updated_at=now,
    )

    with pytest.raises(
        ValueError,
        match="Invalid document status transition: processing -> pending",
    ):
        document.transition_to(DocumentStatus.PENDING)


def test_document_updates_timestamp_on_status_transition():
    created_at = datetime(2026, 1, 1, tzinfo=UTC)
    updated_at = datetime(2026, 1, 1, tzinfo=UTC)

    document = Document(
        id=uuid4(),
        title="Employee Handbook",
        source_type=DocumentSourceType.PDF,
        source_uri="documents/employee-handbook.pdf",
        status=DocumentStatus.PENDING,
        owner_id=uuid4(),
        created_at=created_at,
        updated_at=updated_at,
    )

    created_at_before = document.created_at
    updated_at_before = document.updated_at

    document.transition_to(DocumentStatus.PROCESSING)

    assert document.created_at == created_at_before
    assert document.updated_at > updated_at_before
