"""
Shared Gemini AI client
Every AI feature (chatbot, meals, activity generation) goes through here,
so the whole app needs a single API key: GEMINI_API_KEY.
"""

import json
import os

from google import genai
from google.genai import types

DEFAULT_MODEL = 'gemini-2.5-flash'

_client = None


class AIUnavailableError(RuntimeError):
    """Raised when no Gemini API key is configured"""


def get_api_key():
    """Read the API key (GOOGLE_API_KEY is accepted as a fallback)"""
    return os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')


def get_model():
    """Model name, overridable with GEMINI_MODEL"""
    return os.getenv('GEMINI_MODEL', DEFAULT_MODEL)


def get_client():
    """Return a cached Gemini client"""
    global _client
    if _client is None:
        api_key = get_api_key()
        if not api_key:
            raise AIUnavailableError(
                'GEMINI_API_KEY is not set. Add it to your .env file to enable AI features.'
            )
        _client = genai.Client(api_key=api_key)
    return _client


def generate_text(contents, system_instruction=None, temperature=None, model=None):
    """
    Generate a plain text response

    Args:
        contents: a prompt string, or a list of types.Content for multi-turn chats
        system_instruction: optional system prompt
        temperature: optional sampling temperature
        model: optional model override

    Returns:
        Response text (stripped)
    """
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=temperature,
    )
    response = get_client().models.generate_content(
        model=model or get_model(),
        contents=contents,
        config=config,
    )
    return (response.text or '').strip()


def generate_json(prompt, temperature=None, model=None):
    """
    Generate a JSON response and parse it

    Returns:
        Parsed JSON (dict or list)

    Raises:
        ValueError: if the model did not return valid JSON
    """
    config = types.GenerateContentConfig(
        temperature=temperature,
        response_mime_type='application/json',
    )
    response = get_client().models.generate_content(
        model=model or get_model(),
        contents=prompt,
        config=config,
    )
    return parse_json(response.text or '')


def parse_json(text):
    """Parse JSON, tolerating a surrounding ```json markdown fence"""
    text = text.strip()
    if text.startswith('```'):
        text = text.split('\n', 1)[1] if '\n' in text else ''
        if text.rstrip().endswith('```'):
            text = text.rstrip()[:-3]
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f'AI returned invalid JSON: {e}') from e


def chat_message(role, text):
    """Build a chat turn. role is 'user' or 'model'."""
    return types.Content(role=role, parts=[types.Part(text=text)])
