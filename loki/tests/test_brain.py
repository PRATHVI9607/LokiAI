import json
import pytest
from unittest.mock import MagicMock, patch
from loki.core.brain import LokiBrain


@pytest.fixture
def brain(tmp_path):
    cfg = {
        "llm": {
            "ollama": {"base_url": "http://localhost:11434", "model": "phi3:mini", "timeout": 30},
            "openrouter": {"api_key": "", "model": "meta-llama/llama-3.1-8b-instruct:free", "timeout": 30},
        },
        "memory": {"max_context_turns": 10},
    }
    mem_dir = tmp_path / "memory"
    mem_dir.mkdir()
    with patch("loki.core.brain.MEMORY_DIR", mem_dir):
        b = LokiBrain(cfg)
    return b


def test_parse_intent_plain_json(brain):
    raw = '{"intent": "system_stats", "args": {}}'
    result = brain.parse_intent(raw)
    assert result["intent"] == "system_stats"


def test_parse_intent_markdown_wrapped(brain):
    raw = '```json\n{"intent": "open_app", "args": {"app": "chrome"}}\n```'
    result = brain.parse_intent(raw)
    assert result["intent"] == "open_app"
    assert result["args"]["app"] == "chrome"


def test_parse_intent_invalid_returns_chat(brain):
    result = brain.parse_intent("This is just a sentence.")
    assert result["intent"] == "chat"


def test_store_turn(brain):
    brain._store_turn("user", "hello")
    brain._store_turn("assistant", "hi")
    assert len(brain._history) == 2
    assert brain._history[0]["role"] == "user"
