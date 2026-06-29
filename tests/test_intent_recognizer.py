import pytest
from modules.intent_recognizer import IntentRecognizer

class TestIntentRecognizer:
    def setup_method(self):
        self.recognizer = IntentRecognizer()

    def test_recognize_intent_empty_string(self):
        result = self.recognizer.recognize_intent("")
        assert result == {"intent": "UNKNOWN", "entities": {}}

    def test_recognize_intent_whitespace(self):
        result = self.recognizer.recognize_intent("   ")
        assert result == {"intent": "UNKNOWN", "entities": {}}

    def test_recognize_intent_none(self):
        with pytest.raises(AttributeError):
            self.recognizer.recognize_intent(None)

    def test_recognize_intent_gibberish(self):
        result = self.recognizer.recognize_intent("asdfghjkl")
        assert result == {"intent": "UNKNOWN", "entities": {}}

    def test_recognize_intent_punctuation(self):
        result = self.recognizer.recognize_intent("!!!@@@")
        assert result == {"intent": "UNKNOWN", "entities": {}}

    def test_recognize_intent_numbers_only(self):
        result = self.recognizer.recognize_intent("123456789")
        assert result == {"intent": "UNKNOWN", "entities": {}}

    def test_recognize_intent_unrelated_sentence(self):
        result = self.recognizer.recognize_intent("the quick brown fox jumps over the lazy dog")
        assert result == {"intent": "UNKNOWN", "entities": {}}
