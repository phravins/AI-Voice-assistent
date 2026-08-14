import os
import json
import pytest
from unittest.mock import patch, mock_open
from modules.doc_store import load

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
