from uuid import uuid4

from app.application.processing.contracts.parsed_document import ParsedDocument
from app.domain.entities.document import DocumentSourceType


def test_parsed_document_stores_required_fields():
    document_id = uuid4()
    metadata = {"page_count": 3}

    parsed_document = ParsedDocument(
        document_id=document_id,
        content="Extracted document content",
        source_type=DocumentSourceType.PDF,
        metadata=metadata,
    )

    assert parsed_document.document_id == document_id
    assert parsed_document.content == "Extracted document content"
    assert parsed_document.source_type == DocumentSourceType.PDF
    assert parsed_document.metadata == metadata


def test_parsed_document_metadata_defaults_to_empty_dict():
    parsed_document = ParsedDocument(
        document_id=uuid4(),
        content="Extracted content",
        source_type=DocumentSourceType.TEXT,
    )

    assert parsed_document.metadata == {}


def test_parsed_document_is_immutable():
    parsed_document = ParsedDocument(
        document_id=uuid4(),
        content="Extracted content",
        source_type=DocumentSourceType.TEXT,
    )

    try:
        parsed_document.content = "Modified content"
    except AttributeError:
        pass
    else:
        raise AssertionError("ParsedDocument should be immutable.")