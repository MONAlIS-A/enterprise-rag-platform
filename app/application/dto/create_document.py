from uuid import UUID

from app.domain.entities.document import DocumentSourceType


class CreateDocumentCommand:
    def __init__(
        self,
        title: str,
        source_type: DocumentSourceType,
        source_uri: str,
        owner_id: UUID,
    ) -> None:
        self.title = title
        self.source_type = source_type
        self.source_uri = source_uri
        self.owner_id = owner_id