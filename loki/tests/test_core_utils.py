"""
Tests for the shared utilities added in the #9 quality pass:
log redaction, path validation, and config checking.
"""

from pathlib import Path

from loki.core.log_utils import redact
from loki.core.paths import resolve_within_roots
from loki.core.config_check import validate_config


class TestRedact:
    def test_masks_query_secrets(self):
        out = redact("GET https://api.x/v1?api_key=SECRET123&q=hello")
        assert "SECRET123" not in out
        assert "api_key=***" in out
        assert "q=hello" in out  # non-secret params preserved

    def test_masks_bearer(self):
        out = redact("Authorization: Bearer abcdef0123456789")
        assert "abcdef0123456789" not in out
        assert "Bearer ***" in out

    def test_passthrough_plain(self):
        assert redact("just a normal log line") == "just a normal log line"
        assert redact("") == ""


class TestResolveWithinRoots:
    def test_inside(self, tmp_path):
        ok, resolved = resolve_within_roots(str(tmp_path / "a" / "b.txt"), [tmp_path])
        assert ok is True
        assert resolved.name == "b.txt"

    def test_outside(self, tmp_path):
        ok, _ = resolve_within_roots("C:/Windows/System32/x", [tmp_path])
        assert ok is False

    def test_traversal_escape(self, tmp_path):
        escape = str(tmp_path) + ("/.." * 12) + "/Windows/x"
        ok, _ = resolve_within_roots(escape, [tmp_path])
        assert ok is False

    def test_empty(self, tmp_path):
        assert resolve_within_roots("", [tmp_path])[0] is False


class TestValidateConfig:
    def test_clean_config_has_no_problems(self):
        cfg = {
            "llm": {"temperature": 0.7, "max_tokens": 600, "ollama_timeout": 60,
                    "bandit": {"epsilon": 0.15}},
            "wakeword": {"rms_threshold": 0.0025},
            "audio": {"vad_aggressiveness": 0},
            "ui": {"port": 7777},
            "proactive": {"check_interval": 20},
            "whisper": {"device": "auto"},
        }
        assert validate_config(cfg) == []

    def test_flags_bad_values(self):
        cfg = {
            "llm": {"temperature": 9.0, "bandit": {"epsilon": 5.0}},
            "audio": {"vad_aggressiveness": 7},
            "whisper": {"device": "tpu"},
            "ui": {"port": 999999},
        }
        problems = validate_config(cfg)
        # each bad key should be reported
        joined = " ".join(problems)
        assert "temperature" in joined
        assert "epsilon" in joined
        assert "vad_aggressiveness" in joined
        assert "whisper.device" in joined
        assert "ui.port" in joined

    def test_absent_keys_ok(self):
        # missing keys → defaults apply, no false positives
        assert validate_config({}) == []
