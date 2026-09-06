from uuid import UUID

from app.core.exceptions import AppException


class ProcessingError(AppException):
    """Base exception for document processing failures."""

    def __init__(
        self,
        message: str,
        document_id: UUID,
        stage: str,
        cause: Exception | None = None,
    ) -> None:
        self.document_id = document_id
        self.stage = stage
        self.cause = cause

        super().__init__(
            message=message,
            code="PROCESSING_ERROR",
            status_code=500,
        )


class ParsingError(ProcessingError):
    """Raised when document parsing fails."""

    def __init__(
        self,
        message: str,
        document_id: UUID,
        cause: Exception | None = None,
    ) -> None:
        super().__init__(
            message=message,
            document_id=document_id,
            stage="parsing",
            cause=cause,
        )


class CleaningError(ProcessingError):
    """Raised when document cleaning fails."""

    def __init__(
        self,
        message: str,
        document_id: UUID,
        cause: Exception | None = None,
    ) -> None:
        super().__init__(
            message=message,
            document_id=document_id,
            stage="cleaning",
            cause=cause,
        )


class ChunkingError(ProcessingError):
    """Raised when document chunking fails."""

    def __init__(
        self,
        message: str,
        document_id: UUID,
        cause: Exception | None = None,
    ) -> None:
        super().__init__(
            message=message,
            document_id=document_id,
            stage="chunking",
            cause=cause,
        )


class EmbeddingError(ProcessingError):
    """Raised when document embedding fails."""

    def __init__(
        self,
        message: str,
        document_id: UUID,
        cause: Exception | None = None,
    ) -> None:
        super().__init__(
            message=message,
            document_id=document_id,
            stage="embedding",
            cause=cause,
        )


class IndexingError(ProcessingError):
    """Raised when document indexing fails."""

    def __init__(
        self,
        message: str,
        document_id: UUID,
        cause: Exception | None = None,
    ) -> None:
        super().__init__(
            message=message,
            document_id=document_id,
            stage="indexing",
            cause=cause,
        )