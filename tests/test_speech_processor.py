import pytest
from unittest.mock import patch, MagicMock
import os
import uuid

from modules.speech_processor import SpeechProcessor

@pytest.fixture
def mock_sr():
    with patch('modules.speech_processor.sr') as mock:
        yield mock

def test_speak_text_empty(mock_sr):
    processor = SpeechProcessor()
    with patch('modules.speech_processor.gTTS') as mock_gtts:
        processor.speak_text("")
        mock_gtts.assert_not_called()

def test_speak_text_success(mock_sr):
    processor = SpeechProcessor()

    with patch('modules.speech_processor.gTTS') as mock_gtts, \
         patch('modules.speech_processor.AudioHandler') as mock_audio_handler_class, \
         patch('uuid.uuid4') as mock_uuid4, \
         patch('modules.speech_processor.os.remove') as mock_remove:

        mock_uuid4.return_value.hex = "1234"
        mock_gtts_instance = MagicMock()
        mock_gtts.return_value = mock_gtts_instance

        mock_audio_handler_instance = MagicMock()
        mock_audio_handler_class.return_value = mock_audio_handler_instance

        processor.speak_text("hello", lang="en")

        mock_gtts.assert_called_once_with(text="hello", lang="en", slow=False)

        # We check the arguments passed to tts.save and play_audio_file
        save_args = mock_gtts_instance.save.call_args[0]
        assert save_args[0].endswith("temp_output_1234.mp3")

        mock_audio_handler_instance.play_audio_file.assert_called_once_with(save_args[0])
        mock_audio_handler_instance.cleanup.assert_called_once()
        mock_remove.assert_called_once_with(save_args[0])

def test_speak_text_gtts_exception(mock_sr):
    processor = SpeechProcessor()

    with patch('modules.speech_processor.gTTS', side_effect=Exception("gTTS Error")), \
         patch('modules.speech_processor.AudioHandler') as mock_audio_handler_class:

        processor.speak_text("hello")

        # audio_handler might not be created, or cleanup not called if not created
        # the code uses try-except around audio_handler.cleanup() which fails silently
        mock_audio_handler_class.assert_not_called()

def test_speak_text_audio_handler_exception(mock_sr):
    processor = SpeechProcessor()

    with patch('modules.speech_processor.gTTS') as mock_gtts, \
         patch('modules.speech_processor.AudioHandler') as mock_audio_handler_class, \
         patch('modules.speech_processor.os.remove') as mock_remove:

        mock_audio_handler_instance = MagicMock()
        mock_audio_handler_class.return_value = mock_audio_handler_instance
        mock_audio_handler_instance.play_audio_file.side_effect = Exception("Audio Play Error")

        processor.speak_text("hello")

        mock_audio_handler_instance.cleanup.assert_called_once()
        mock_remove.assert_not_called()

def test_speak_text_os_remove_exception(mock_sr):
    processor = SpeechProcessor()

    with patch('modules.speech_processor.gTTS') as mock_gtts, \
         patch('modules.speech_processor.AudioHandler') as mock_audio_handler_class, \
         patch('modules.speech_processor.os.remove', side_effect=OSError("Remove Error")) as mock_remove:

        mock_audio_handler_instance = MagicMock()
        mock_audio_handler_class.return_value = mock_audio_handler_instance

        processor.speak_text("hello")

        # should still call cleanup and remove, and not crash
        mock_audio_handler_instance.cleanup.assert_called_once()
        mock_remove.assert_called_once()
