import os
import json
import pytest
from unittest.mock import patch, mock_open

os.environ['GEMINI_API_KEY'] = 'test_key'

from modules.doc_store import load, save
from config import DOCS_DIR

@patch("os.path.exists")
@patch("builtins.open", new_callable=mock_open, read_data='{"title": "Test Doc", "content": "This is a test."}')
def test_load_existing_doc(mock_file, mock_exists):
    # Setup
    mock_exists.return_value = True
    doc_id = "test_doc_123"

    # Execute
    result = load(doc_id)

    # Assert
    assert result == {"title": "Test Doc", "content": "This is a test."}
    # verify that exist check happened
    mock_exists.assert_called_once()
    # verify that open happened
    mock_file.assert_called_once()

@patch("os.path.exists")
def test_load_nonexistent_doc(mock_exists):
    # Setup
    mock_exists.return_value = False
    doc_id = "missing_doc"

    # Execute
    result = load(doc_id)

    # Assert
    assert result == {}
    mock_exists.assert_called_once()


def test_save_with_custom_id():
    doc_structure = {"title": "Test Doc", "content": "Hello World"}
    custom_id = "my-custom-id"
    expected_path = "/mocked/path/my-custom-id.json"

    with patch("builtins.open", mock_open()) as mocked_open:
        with patch("modules.doc_store.json.dump") as mocked_json_dump:
            with patch("modules.doc_store.os.path.join", return_value=expected_path) as mocked_join:
                doc_id = save(doc_structure, custom_id=custom_id)

                assert doc_id == custom_id
                mocked_join.assert_called_once_with(DOCS_DIR, f"{custom_id}.json")
                mocked_open.assert_called_once_with(expected_path, "w", encoding="utf-8")
                mocked_json_dump.assert_called_once_with(doc_structure, mocked_open(), ensure_ascii=False)


def test_save_without_custom_id():
    doc_structure = {"title": "Another Doc", "content": "Hello again"}
    expected_path = "/mocked/path/test-uuid-hex.json"

    with patch("builtins.open", mock_open()) as mocked_open:
        with patch("modules.doc_store.json.dump") as mocked_json_dump:
            with patch("modules.doc_store.os.path.join", return_value=expected_path) as mocked_join:
                with patch("modules.doc_store.uuid.uuid4") as mocked_uuid:
                    mocked_uuid.return_value.hex = "test-uuid-hex"

                    doc_id = save(doc_structure)

                    assert doc_id == "test-uuid-hex"
                    mocked_join.assert_called_once_with(DOCS_DIR, "test-uuid-hex.json")
                    mocked_open.assert_called_once_with(expected_path, "w", encoding="utf-8")
                    mocked_json_dump.assert_called_once_with(doc_structure, mocked_open(), ensure_ascii=False)
