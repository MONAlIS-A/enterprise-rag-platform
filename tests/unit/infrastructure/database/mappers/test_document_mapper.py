from datetime import UTC, datetime
from uuid import uuid4

from app.domain.entities.document import (
    Document,
    DocumentSourceType,
    DocumentStatus,
)
from app.infrastructure.database.mappers.document_mapper import (
    to_entity,
    to_model,
)


def create_document() -> Document:
    timestamp = datetime(2026, 1, 1, tzinfo=UTC)

    return Document(
        id=uuid4(),
        title="Employee Handbook",
        source_type=DocumentSourceType.PDF,
        source_uri="documents/employee-handbook.pdf",
        status=DocumentStatus.PENDING,
        owner_id=uuid4(),
        created_at=timestamp,
        updated_at=timestamp,
    )


def test_to_model_maps_domain_entity_to_persistence_model():
    document = create_document()

    model = to_model(document)

    assert model.id == document.id
    assert model.title == document.title
    assert model.source_type == document.source_type.value
    assert model.source_uri == document.source_uri
    assert model.status == document.status.value
    assert model.owner_id == document.owner_id
    assert model.created_at == document.created_at
    assert model.updated_at == document.updated_at


def test_to_entity_maps_persistence_model_to_domain_entity():
    document = create_document()
    model = to_model(document)

    restored_document = to_entity(model)

    assert restored_document.id == document.id
    assert restored_document.title == document.title
    assert restored_document.source_type == document.source_type
    assert restored_document.source_uri == document.source_uri
    assert restored_document.status == document.status
    assert restored_document.owner_id == document.owner_id
    assert restored_document.created_at == document.created_at
    assert restored_document.updated_at == document.updated_at


def test_document_mapping_round_trip_preserves_domain_data():
    original_document = create_document()

    model = to_model(original_document)
    restored_document = to_entity(model)

    assert restored_document == original_document
