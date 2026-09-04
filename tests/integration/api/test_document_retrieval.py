from uuid import uuid4
from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.infrastructure.database.models.document import DocumentModel
from app.infrastructure.database.session import SessionLocal
from app.main import app


client = TestClient(app)


def test_get_document_api():
    owner_id = uuid4()
    document_id = uuid4()

    session = SessionLocal()

    try:
        document = DocumentModel(
            id=document_id,
            title="Retrieval Integration Test Document",
            source_type="text",
            source_uri="test://api/retrieval-document",
            status="pending",
            owner_id=owner_id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        session.add(document)
        session.commit()

        response = client.get(f"/documents/{document_id}")

        assert response.status_code == 200

        data = response.json()

        assert data["id"] == str(document_id)
        assert data["title"] == document.title
        assert data["source_type"] == document.source_type
        assert data["source_uri"] == document.source_uri
        assert data["status"] == document.status
        assert data["owner_id"] == str(owner_id)

    finally:
        session.query(DocumentModel).filter(
            DocumentModel.id == document_id
        ).delete()
        session.commit()
        session.close()


def test_get_document_api_returns_404_for_missing_document():
    document_id = uuid4()

    response = client.get(f"/documents/{document_id}")

    assert response.status_code == 404

    data = response.json()

    assert data["error"]["code"] == "NOT_FOUND"

def test_get_document_api_rejects_invalid_uuid():
    response = client.get("/documents/not-a-valid-uuid")

    assert response.status_code == 422