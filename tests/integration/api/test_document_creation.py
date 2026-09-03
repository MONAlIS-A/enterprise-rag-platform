from uuid import uuid4

from fastapi.testclient import TestClient

from app.infrastructure.database.models.document import DocumentModel
from app.infrastructure.database.session import SessionLocal
from app.main import app


client = TestClient(app)


def test_create_document_api():
    owner_id = uuid4()

    payload = {
        "title": "API Integration Test Document",
        "source_type": "text",
        "source_uri": "test://api/document",
        "owner_id": str(owner_id),
    }

    response = client.post("/documents", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == payload["title"]
    assert data["source_type"] == payload["source_type"]
    assert data["source_uri"] == payload["source_uri"]
    assert data["owner_id"] == payload["owner_id"]
    assert data["status"] == "pending"

    document_id = data["id"]

    session = SessionLocal()

    try:
        persisted_document = session.get(DocumentModel, document_id)

        assert persisted_document is not None
        assert str(persisted_document.id) == document_id

    finally:
        session.query(DocumentModel).filter(
            DocumentModel.id == document_id
        ).delete()
        session.commit()
        session.close()


def test_create_document_api_rejects_invalid_request():
    payload = {
        "title": "",
        "source_type": "text",
        "source_uri": "test://api/document",
        "owner_id": str(uuid4()),
    }

    response = client.post("/documents", json=payload)

    assert response.status_code == 422