import os
import pytest
from unittest.mock import patch, MagicMock

# Set environment variable before importing to bypass config.py ValueError
os.environ["GEMINI_API_KEY"] = "fake-test-key"

# Import to ensure modules.gemini_client is available for patch
import modules.gemini_client

@pytest.fixture
def mock_genai():
    with patch('modules.gemini_client.genai.configure') as mock_configure, \
         patch('modules.gemini_client.genai.GenerativeModel') as mock_generative_model:
        yield mock_configure, mock_generative_model

@pytest.fixture
def gemini_client(mock_genai):
    from modules.gemini_client import GeminiClient
    return GeminiClient()

def test_build_prompt_summarize(gemini_client):
    context = "This is a test context."
    prompt = gemini_client._build_prompt("SUMMARIZE", context)

    assert "You are an AI Voice Tutor." in prompt
    assert "ROLE: Patient Teacher" in prompt
    assert context in prompt
    assert "Write a single cohesive paragraph summary (6–9 sentences) in simple, clear language." in prompt
    assert "bullet points or lists" in prompt

def test_build_prompt_explain_with_question(gemini_client):
    context = "Photosynthesis is a process."
    question = "What is chlorophyll?"
    prompt = gemini_client._build_prompt("EXPLAIN", context, user_question=question)

    assert "You are an AI Voice Tutor." in prompt
    assert "ROLE: Patient Teacher" in prompt
    assert context in prompt
    assert "Explain the following concept step by step in simple terms, with examples." in prompt
    assert f"QUESTION: {question}" in prompt

def test_build_prompt_explain_without_question(gemini_client):
    context = "Photosynthesis is a process."
    prompt = gemini_client._build_prompt("EXPLAIN", context)

    assert "You are an AI Voice Tutor." in prompt
    assert "ROLE: Patient Teacher" in prompt
    assert context in prompt
    assert "Explain the following concept step by step in simple terms, with examples." in prompt
    assert "QUESTION: " not in prompt

def test_build_prompt_translate(gemini_client):
    context = "Hello world."
    target_language = "Spanish"
    prompt = gemini_client._build_prompt("TRANSLATE", context, target_language=target_language)

    assert "You are an AI Voice Tutor." in prompt
    assert "ROLE: Translator" in prompt
    assert context in prompt
    assert f"Translate the text into {target_language}." in prompt

def test_build_prompt_quiz(gemini_client):
    context = "Python is a programming language."
    difficulty = "hard"
    prompt = gemini_client._build_prompt("QUIZ", context, difficulty=difficulty)

    assert "You are an AI Voice Tutor." in prompt
    assert "ROLE: Quiz Master" in prompt
    assert context in prompt
    assert f"Create 3 {difficulty} difficulty quiz questions" in prompt
    assert "strict JSON format" in prompt

def test_build_prompt_default_fallback(gemini_client):
    context = "Some context here."
    intent = "DANCE"
    prompt = gemini_client._build_prompt(intent, context)

    assert "You are an AI Voice Tutor." in prompt
    assert "ROLE: Assistant" in prompt
    assert context in prompt
    assert f"The user has a command related to this content: {intent}." in prompt
