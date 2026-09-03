from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from uuid import UUID


class DocumentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"
    ARCHIVED = "archived"


class DocumentSourceType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    URL = "url"
    TEXT = "text"


@dataclass
class Document:
    id: UUID
    title: str
    source_type: DocumentSourceType
    source_uri: str
    status: DocumentStatus
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("Document title cannot be empty.")

        if not self.source_uri.strip():
            raise ValueError("Document source URI cannot be empty.")

    def transition_to(self, new_status: DocumentStatus) -> None:
        allowed_transitions = {
            DocumentStatus.PENDING: {
                DocumentStatus.PROCESSING,
            },
            DocumentStatus.PROCESSING: {
                DocumentStatus.READY,
                DocumentStatus.FAILED,
            },
            DocumentStatus.READY: {
                DocumentStatus.ARCHIVED,
            },
            DocumentStatus.FAILED: set(),
            DocumentStatus.ARCHIVED: set(),
        }

        if new_status not in allowed_transitions[self.status]:
            raise ValueError(
                f"Invalid document status transition: "
                f"{self.status.value} -> {new_status.value}"
            )

        self.status = new_status
        self.updated_at = datetime.now(timezone.utc)