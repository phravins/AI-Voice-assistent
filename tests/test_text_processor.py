import pytest
from modules.text_processor import clean_text

def test_clean_text():
    # Test None and empty string
    assert clean_text(None) == ""
    assert clean_text("") == ""

    # Test normal string without extra spaces
    assert clean_text("Hello world") == "Hello world"

    # Test string with multiple contiguous spaces
    assert clean_text("Hello    world") == "Hello world"

    # Test string with newlines and tabs
    assert clean_text("Hello\nworld") == "Hello world"
    assert clean_text("Hello\tworld") == "Hello world"
    assert clean_text("Hello \n \t world") == "Hello world"

    # Test string with leading and trailing spaces
    assert clean_text("  Hello world  ") == "Hello world"

    # Mixed scenario
    assert clean_text("  This \n is \t a   test.  ") == "This is a test."
