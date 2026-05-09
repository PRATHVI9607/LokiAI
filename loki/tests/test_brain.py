import pytest
from unittest.mock import MagicMock, patch
from loki.core.brain import LokiBrain


@pytest.fixture
def brain(tmp_path):
    mem_dir = tmp_path / "memory"
    mem_dir.mkdir()
    cfg = {
        "ollama_model": "phi3:mini",
        "fallback_model": "meta-llama/llama-3.1-8b-instruct:free",
        "second_fallback_model": "microsoft/phi-3-mini-128k-instruct:free",
        "max_tokens": 100,
        "temperature": 0.7,
        "max_turns": 10,
    }
    # Patch OpenAI so no real network calls are made
    with patch("loki.core.brain.OpenAI") as mock_openai_cls:
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        # Ollama list call succeeds so it marks itself available
        mock_client.models.list.return_value = []
        b = LokiBrain(cfg, mem_dir)
    return b


def test_parse_intent_plain_json(brain):
    raw = '{"intent": "system_stats", "args": {}}'
    result = brain.parse_intent(raw)
    assert result is not None
    assert result["intent"] == "system_stats"


def test_parse_intent_markdown_wrapped(brain):
    raw = '```json\n{"intent": "open_app", "args": {"app": "chrome"}}\n```'
    result = brain.parse_intent(raw)
    assert result is not None
    assert result["intent"] == "open_app"


def test_parse_intent_invalid_returns_none(brain):
    result = brain.parse_intent("This is just a sentence.")
    assert result is None


def test_parse_intent_missing_intent_key(brain):
    result = brain.parse_intent('{"action": "something"}')
    assert result is None


def test_store_turn(brain):
    brain._store_turn("what is the weather", "I have no idea, I am indoors.")
    assert len(brain._conversation_history) == 2
    assert brain._conversation_history[0]["role"] == "user"
    assert brain._conversation_history[1]["role"] == "assistant"


def test_clear_conversation(brain):
    brain._store_turn("hello", "hi there")
    brain.clear_conversation()
    assert len(brain._conversation_history) == 0
