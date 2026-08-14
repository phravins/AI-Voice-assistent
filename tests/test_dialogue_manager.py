import pytest
import os
from unittest.mock import patch, call
from modules.dialogue_manager import cleanup_temp_audio

@patch('modules.dialogue_manager.TEMP_AUDIO_DIR', '/tmp/mock_audio_dir')
@patch('modules.dialogue_manager.os.remove')
@patch('modules.dialogue_manager.os.listdir')
@patch('modules.dialogue_manager.logger')
def test_cleanup_temp_audio_success(mock_logger, mock_listdir, mock_remove):
    # Setup mock files
    mock_listdir.return_value = ['file1.mp3', 'file2.txt', 'file3.mp3']

    # Call the function
    cleanup_temp_audio()

    # Assertions
    mock_listdir.assert_called_once_with('/tmp/mock_audio_dir')

    # Ensure os.remove is called only for .mp3 files
    expected_calls = [
        call(os.path.join('/tmp/mock_audio_dir', 'file1.mp3')),
        call(os.path.join('/tmp/mock_audio_dir', 'file3.mp3'))
    ]
    mock_remove.assert_has_calls(expected_calls, any_order=True)
    assert mock_remove.call_count == 2

    # Ensure logger.info is called
    assert mock_logger.info.call_count == 2

@patch('modules.dialogue_manager.TEMP_AUDIO_DIR', '/tmp/mock_audio_dir')
@patch('modules.dialogue_manager.os.remove')
@patch('modules.dialogue_manager.os.listdir')
@patch('modules.dialogue_manager.logger')
def test_cleanup_temp_audio_exception(mock_logger, mock_listdir, mock_remove):
    # Setup mock files
    mock_listdir.return_value = ['error_file.mp3']

    # Simulate os.remove raising an exception
    mock_remove.side_effect = Exception("Mocked delete error")

    # Call the function
    cleanup_temp_audio()

    # Assertions
    expected_path = os.path.join('/tmp/mock_audio_dir', 'error_file.mp3')
    mock_remove.assert_called_once_with(expected_path)

    # Ensure logger.error is called
    mock_logger.error.assert_called_once()
    error_msg = mock_logger.error.call_args[0][0]
    assert f"Could not delete temporary file {expected_path}" in error_msg
