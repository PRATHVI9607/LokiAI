"""
Tests for the second hardening pass: task recurrence, knowledge-graph pruning,
JSON log formatter, listener worker watchdog, and the brain LLM lock.
"""

import json
import logging
from unittest.mock import MagicMock

import pytest


# ── Task recurrence (Issue #4) ───────────────────────────────────────────────

class TestTaskRecurrence:
    def _mem(self, tmp_path):
        from loki.core.memory import MemoryManager
        return MemoryManager(tmp_path)

    def test_completing_recurring_task_spawns_next(self, tmp_path):
        mem = self._mem(tmp_path)
        t = mem.add_task("standup", "high", due="2026-06-01T09:00:00", recurrence="daily")
        open_before = len(mem.list_tasks())
        assert mem.complete_task(t["id"]) is True
        active = mem.list_tasks()  # excludes completed
        # the original is completed; a fresh recurring instance was created
        assert len(active) == open_before
        nxt = active[-1]
        assert nxt["recurrence"] == "daily"
        assert nxt["due"].startswith("2026-06-02")

    def test_non_recurring_does_not_respawn(self, tmp_path):
        mem = self._mem(tmp_path)
        t = mem.add_task("one off", "low")
        mem.complete_task(t["id"])
        assert mem.list_tasks() == []  # nothing regenerated

    def test_manager_rejects_bad_recurrence(self):
        from loki.features.task_manager import TaskManager
        tm = TaskManager(MagicMock())
        res = tm.add("x", recurrence="hourly")
        assert res["success"] is False


# ── Knowledge-graph pruning (Issue #6) ───────────────────────────────────────

def test_kg_prune_caps_edges(tmp_path, monkeypatch):
    from loki.features import knowledge_graph as kg
    monkeypatch.setattr(kg, "MAX_EDGES", 10)
    monkeypatch.setattr(kg, "MAX_NODES", 10)
    g = kg.KnowledgeGraph(graph_path=str(tmp_path / "g.json"))
    g._nodes = {f"n{i}": {"name": f"n{i}"} for i in range(50)}
    g._edges = [{"from": f"n{i}", "to": f"n{i+1}", "relation": "r"} for i in range(50)]
    g._prune()
    assert len(g._edges) <= 10
    assert len(g._nodes) <= 10


# ── JSON log formatter (Issue #9) ────────────────────────────────────────────

def test_json_formatter_emits_valid_json_and_redacts():
    from loki.core.log_setup import JsonFormatter
    rec = logging.LogRecord("loki.test", logging.INFO, __file__, 10,
                            "open https://x/v1?token=SECRETXYZ", None, None)
    line = JsonFormatter().format(rec)
    obj = json.loads(line)
    assert obj["level"] == "INFO"
    assert obj["logger"] == "loki.test"
    assert "SECRETXYZ" not in obj["message"]  # redacted
    assert "token=***" in obj["message"]


# ── Listener worker watchdog (Issue #1) ──────────────────────────────────────

def test_listener_ensure_worker_revives(monkeypatch):
    # Build a SpeechListener without loading Whisper (patch availability off).
    from loki.core import listener as L
    monkeypatch.setattr(L, "WHISPER_AVAILABLE", False)
    sl = L.SpeechListener({"audio": {}, "whisper": {}})
    first = sl._worker
    assert first is not None and first.is_alive()
    # Simulate the worker dying, then ensure it's revived.
    sl._worker = None
    sl._ensure_worker()
    assert sl._worker is not None and sl._worker.is_alive()


# ── Brain LLM lock exists and serializes (Arch) ──────────────────────────────

def test_brain_has_llm_lock():
    import threading
    from loki.core.brain import LokiBrain
    import inspect
    # _call_llm acquires the lock then delegates to _call_llm_locked
    src = inspect.getsource(LokiBrain._call_llm)
    assert "_llm_lock" in src and "_call_llm_locked" in src
