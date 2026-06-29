import pytest
from modules.intent_recognizer import IntentRecognizer

@pytest.fixture
def recognizer():
    return IntentRecognizer()

def test_empty_input(recognizer):
    assert recognizer.recognize_intent("") == {"intent": "UNKNOWN", "entities": {}}
    assert recognizer.recognize_intent("   ") == {"intent": "UNKNOWN", "entities": {}}
    assert recognizer.recognize_intent("\n\t") == {"intent": "UNKNOWN", "entities": {}}

def test_unknown_intent(recognizer):
    assert recognizer.recognize_intent("do some random thing") == {"intent": "UNKNOWN", "entities": {}}
    assert recognizer.recognize_intent("hello world") == {"intent": "UNKNOWN", "entities": {}}

def test_simple_intents(recognizer):
    # SUMMARIZE
    assert recognizer.recognize_intent("please summarize this")["intent"] == "SUMMARIZE"
    assert recognizer.recognize_intent("what is the summary")["intent"] == "SUMMARIZE"

    # EXPLAIN
    assert recognizer.recognize_intent("explain this to me")["intent"] == "EXPLAIN"
    assert recognizer.recognize_intent("define this concept")["intent"] == "EXPLAIN"

    # NAVIGATE_NEXT
    assert recognizer.recognize_intent("go to next page")["intent"] == "NAVIGATE_NEXT"
    assert recognizer.recognize_intent("next")["intent"] == "NAVIGATE_NEXT"

    # NAVIGATE_PREV
    assert recognizer.recognize_intent("go to previous")["intent"] == "NAVIGATE_PREV"
    assert recognizer.recognize_intent("back")["intent"] == "NAVIGATE_PREV"

    # REPEAT
    assert recognizer.recognize_intent("repeat that please")["intent"] == "REPEAT"
    assert recognizer.recognize_intent("say again")["intent"] == "REPEAT"

    # STOP
    assert recognizer.recognize_intent("stop reading")["intent"] == "STOP"
    assert recognizer.recognize_intent("quit the app")["intent"] == "STOP"

    # HELP
    assert recognizer.recognize_intent("i need help")["intent"] == "HELP"
    assert recognizer.recognize_intent("what are your capabilities")["intent"] == "HELP"

def test_navigate_page_intent(recognizer):
    result = recognizer.recognize_intent("go to page 5")
    assert result["intent"] == "NAVIGATE_PAGE"
    assert result["entities"] == {"target_page": 4} # 0-indexed

    result = recognizer.recognize_intent("read page 10")
    assert result["intent"] == "NAVIGATE_PAGE"
    assert result["entities"] == {"target_page": 9}

    # Malformed extraction fallback
    result = recognizer.recognize_intent("go to page") # Missing number, should not match pattern
    assert result["intent"] == "UNKNOWN"

def test_explain_line_intent(recognizer):
    result = recognizer.recognize_intent("explain line 15")
    assert result["intent"] == "EXPLAIN_LINE"
    assert result["entities"] == {"target_line": 14}

    result = recognizer.recognize_intent("detail line 3")
    assert result["intent"] == "EXPLAIN_LINE"
    assert result["entities"] == {"target_line": 2}

def test_read_paragraph_intent(recognizer):
    result = recognizer.recognize_intent("read paragraph 2")
    assert result["intent"] == "READ_PARAGRAPH"
    assert result["entities"] == {"target_paragraph": 1}

    result = recognizer.recognize_intent("paragraph 5")
    assert result["intent"] == "READ_PARAGRAPH"
    assert result["entities"] == {"target_paragraph": 4}

def test_translate_intent(recognizer):
    # Default translation
    result = recognizer.recognize_intent("translate this text")
    assert result["intent"] == "TRANSLATE"
    assert result["entities"] == {"target_language": "English"}

    # Specific language extraction
    result = recognizer.recognize_intent("translate to french")
    assert result["intent"] == "TRANSLATE"
    assert result["entities"] == {"target_language": "French"}

    result = recognizer.recognize_intent("speak in spanish")
    assert result["intent"] == "TRANSLATE"
    assert result["entities"] == {"target_language": "Spanish"}

def test_quiz_intent(recognizer):
    # Default difficulty
    result = recognizer.recognize_intent("test me on this")
    assert result["intent"] == "QUIZ"
    assert result["entities"] == {"difficulty": "medium"}

    # Easy difficulty
    result = recognizer.recognize_intent("give me an easy quiz")
    assert result["intent"] == "QUIZ"
    assert result["entities"] == {"difficulty": "easy"}

    # Hard difficulty
    result = recognizer.recognize_intent("ask me a hard question")
    assert result["intent"] == "QUIZ"
    assert result["entities"] == {"difficulty": "hard"}
