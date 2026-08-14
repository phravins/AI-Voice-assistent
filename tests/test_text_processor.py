import pytest
from modules.text_processor import get_text_chunk, clean_text, combine_doc_text

# get_text_chunk tests (from main branch)
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


# clean_text tests (from main branch)
def test_clean_text_basic():
    text = "  This   is \n a test.  "
    expected = "This is a test."
    assert clean_text(text) == expected


def test_clean_text_empty():
    assert clean_text("") == ""
    assert clean_text(None) == ""


# combine_doc_text tests (merged from both branches)

def test_combine_doc_text_pages():
    """Test combining a simple document structure where pages contain chunks joined by space and pages by double newline."""
    doc_structure = {
        1: ["Page 1 Chunk 0", "Page 1 Chunk 1"],
        2: ["Page 2 Chunk 0"]
    }
    expected = "Page 1 Chunk 0 Page 1 Chunk 1\n\nPage 2 Chunk 0"
    assert combine_doc_text(doc_structure) == expected


def test_combine_doc_text_simple_structure():
    """Test combining a simple document structure (from PR branch)."""
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


def test_combine_doc_text_max_chars_pages():
    """Test truncation with max_chars using pages example."""
    doc_structure = {
        1: ["Hello World"],
        2: ["Next Page"]
    }
    # "Hello World\n\nNext Page" length > 11 so truncated to first page
    assert combine_doc_text(doc_structure, max_chars=11) == "Hello World"


def test_combine_doc_text_max_chars_long_sentence():
    """Test truncation with max_chars using a long sentence example (from PR branch)."""
    doc = {
        1: ["This", "is", "a", "long", "sentence"]
    }
    result = combine_doc_text(doc, max_chars=10)
    assert result == "This is a "


def test_combine_doc_text_empty_doc():
    """Test with an empty document."""
    assert combine_doc_text({}) == ""