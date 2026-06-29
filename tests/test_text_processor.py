import pytest
from modules.text_processor import get_text_chunk, clean_text, combine_doc_text

def test_get_text_chunk_basic():
    doc_structure = {
        1: ["Chunk 0", "Chunk 1"],
        2: ["Page 2 Chunk 0"]
    }
    # Test integer key
    assert get_text_chunk(doc_structure, 1, 0) == "Chunk 0"
    assert get_text_chunk(doc_structure, 1, 1) == "Chunk 1"
    # Test default chunk_index
    assert get_text_chunk(doc_structure, 2) == "Page 2 Chunk 0"

def test_get_text_chunk_string_keys():
    doc_structure = {
        "1": ["Chunk 0", "Chunk 1"],
        "2": ["Page 2 Chunk 0"]
    }
    # Test string key with integer page_num input
    assert get_text_chunk(doc_structure, 1, 0) == "Chunk 0"
    assert get_text_chunk(doc_structure, 2, 0) == "Page 2 Chunk 0"

def test_get_text_chunk_missing_page():
    doc_structure = {1: ["Chunk 0"]}
    assert get_text_chunk(doc_structure, 3) is None

def test_get_text_chunk_out_of_bounds():
    doc_structure = {1: ["Chunk 0"]}
    # Index too large
    assert get_text_chunk(doc_structure, 1, 1) is None
    # Index negative
    assert get_text_chunk(doc_structure, 1, -1) is None

def test_clean_text_basic():
    text = "  This   is \n a test.  "
    expected = "This is a test."
    assert clean_text(text) == expected

def test_clean_text_empty():
    assert clean_text("") == ""
    assert clean_text(None) == ""

def test_combine_doc_text_basic():
    doc_structure = {
        1: ["Page 1 Chunk 0", "Page 1 Chunk 1"],
        2: ["Page 2 Chunk 0"]
    }
    # Page chunks are joined by space, pages joined by \n\n
    expected = "Page 1 Chunk 0 Page 1 Chunk 1\n\nPage 2 Chunk 0"
    assert combine_doc_text(doc_structure) == expected

def test_combine_doc_text_sorting():
    doc_structure = {
        "10": ["Page 10"],
        "2": ["Page 2"],
        1: ["Page 1"]
    }
    # Should sort numerically: 1, 2, 10
    expected = "Page 1\n\nPage 2\n\nPage 10"
    assert combine_doc_text(doc_structure) == expected

def test_combine_doc_text_max_chars():
    doc_structure = {
        1: ["Hello World"],
        2: ["Next Page"]
    }
    # "Hello World\n\nNext Page" is length 11 + 2 + 9 = 22
    assert combine_doc_text(doc_structure, max_chars=11) == "Hello World"
