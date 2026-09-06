from uuid import uuid4

import pytest

from app.application.processing.errors import (
    ChunkingError,
    CleaningError,
    EmbeddingError,
    IndexingError,
    ParsingError,
    ProcessingError,
)


def test_parsing_error_contains_structured_failure_information():
    document_id = uuid4()
    cause = ValueError("Corrupted PDF")

    error = ParsingError(
        message="Failed to parse document.",
        document_id=document_id,
        cause=cause,
    )

    assert isinstance(error, ProcessingError)
    assert error.message == "Failed to parse document."
    assert error.document_id == document_id
    assert error.stage == "parsing"
    assert error.cause is cause
    assert error.code == "PROCESSING_ERROR"


@pytest.mark.parametrize(
    ("error_class", "expected_stage"),
    [
        (CleaningError, "cleaning"),
        (ChunkingError, "chunking"),
        (EmbeddingError, "embedding"),
        (IndexingError, "indexing"),
    ],
)
def test_processing_error_subclasses_are_processing_errors(
    error_class,
    expected_stage,
):
    document_id = uuid4()

    error = error_class(
        message="Processing stage failed.",
        document_id=document_id,
    )

    assert isinstance(error, ProcessingError)
    assert error.document_id == document_id
    assert error.stage == expected_stage