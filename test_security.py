import pytest
import os
from unittest.mock import MagicMock

# Mock pymongo to avoid requiring a running MongoDB
import pymongo
pymongo.MongoClient = MagicMock()

from web_app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_delete_document_valid(client):
    # Simulate a valid file deletion scenario
    from config import UPLOADS_DIR
    import uuid
    dummy_id = uuid.uuid4().hex
    dummy_path = os.path.join(UPLOADS_DIR, f"{dummy_id}.pdf")

    with open(dummy_path, "w") as f:
        f.write("dummy pdf")

    response = client.delete(f"/api/library/{dummy_id}")
    assert response.status_code == 200
    assert response.json["message"] == "Document deleted"
    assert not os.path.exists(dummy_path)

def test_delete_document_invalid_not_found(client):
    response = client.delete("/api/library/non_existent_file_123")
    assert response.status_code == 404
    assert response.json["error"] == "File not found"

def test_delete_document_path_traversal_direct():
    with app.app_context():
        # Call the endpoint directly with a path traversal payload
        from web_app import api_delete_document
        response, status_code = api_delete_document("../../../some_secret_file")
        assert status_code == 400
        assert response.json["error"] == "Invalid document ID"

if __name__ == "__main__":
    pytest.main(["-v", "test_security.py"])
