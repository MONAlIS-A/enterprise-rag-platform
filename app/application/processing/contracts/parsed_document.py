from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from app.domain.entities.document import DocumentSourceType


@dataclass(frozen=True)
class ParsedDocument:
    document_id: UUID
    content: str
    source_type: DocumentSourceType
    metadata: dict[str, Any] = field(default_factory=dict)