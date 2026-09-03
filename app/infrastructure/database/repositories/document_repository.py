from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.document import Document
from app.domain.repositories.document_repository import DocumentRepository
from app.infrastructure.database.mappers.document_mapper import to_entity, to_model
from app.infrastructure.database.models.document import DocumentModel


class SqlAlchemyDocumentRepository(DocumentRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, document: Document) -> Document:
        model = to_model(document)

        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)

        return to_entity(model)

    def get_by_id(self, document_id: UUID) -> Document | None:
        statement = select(DocumentModel).where(
            DocumentModel.id == document_id
        )

        model = self.session.scalar(statement)

        if model is None:
            return None

        return to_entity(model)