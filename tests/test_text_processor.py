import pytest
from modules.text_processor import combine_doc_text

def test_combine_doc_text_basic():
    """Test combining a simple document structure."""
    doc = {
        1: ["Hello", "world"],
        2: ["This", "is", "page", "two"]
    }
    result = combine_doc_text(doc)
    assert result == "Hello world\n\nThis is page two"

def test_combine_doc_text_string_keys():
    """Test combining with string keys."""
    doc = {
        "1": ["Hello", "world"],
        "2": ["This", "is", "page", "two"]
    }
    result = combine_doc_text(doc)
    assert result == "Hello world\n\nThis is page two"

def test_combine_doc_text_out_of_order_keys():
    """Test combining with out of order keys (should sort by int)."""
    doc = {
        3: ["Page", "three"],
        1: ["Page", "one"],
        "2": ["Page", "two"]
    }
    result = combine_doc_text(doc)
    assert result == "Page one\n\nPage two\n\nPage three"

def test_combine_doc_text_empty_chunks():
    """Test combining with empty chunks or pages."""
    doc = {
        1: ["Hello", ""],
        2: [],
        3: ["world"]
    }
    result = combine_doc_text(doc)
    # Page 1 has one non-empty chunk: "Hello"
    # Page 2 has no chunks, so it is skipped.
    assert result == "Hello\n\nworld"

def test_combine_doc_text_none_values():
    """Test combining with None chunks."""
    doc = {
        1: ["Hello", None, "world"]
    }
    result = combine_doc_text(doc)
    assert result == "Hello world"

def test_combine_doc_text_max_chars():
    """Test truncation with max_chars."""
    doc = {
        1: ["This", "is", "a", "long", "sentence"]
    }
    result = combine_doc_text(doc, max_chars=10)
    assert result == "This is a "

def test_combine_doc_text_empty_doc():
    """Test with an empty document."""
    assert combine_doc_text({}) == ""
