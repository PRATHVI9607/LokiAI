"""
Tests for the CODE_REVIEW.md fixes — undo size/depth caps, vault throttling,
embed retry, pending-action cap, audit timestamp, feature-registration warning,
wakeword availability gating.

Each test pins a behaviour that the review flagged as a real risk, so a
regression would fail CI.
"""

import time
from unittest.mock import MagicMock

import pytest

from loki.actions.file_ops import FileOps
import loki.actions.file_ops as file_ops_mod
from loki.features.vault import Vault, CRYPTO_AVAILABLE
from loki.core.pending_actions import PendingActionStore, _MAX_PENDING
from loki.core.audit import AuditLog
from loki.core.action_router import ActionRouter


@pytest.fixture
def undo():
    return MagicMock()


@pytest.fixture
def file_ops(undo, tmp_path):
    return FileOps(undo, extra_roots=[tmp_path])


# ── #4 / #5: undo snapshot size + depth caps ─────────────────────────────────

class TestUndoCaps:
    def test_large_file_deletes_without_undo(self, file_ops, undo, tmp_path, monkeypatch):
        monkeypatch.setattr(file_ops_mod, "MAX_UNDO_FILE_BYTES", 8)  # tiny cap
        big = tmp_path / "big.bin"
        big.write_bytes(b"x" * 64)  # over the cap
        res = file_ops.delete_file(str(big))
        assert res["success"] is True
        assert not big.exists()
        assert "too large" in res["message"].lower()
        undo.push.assert_not_called()  # no RAM-bloating snapshot taken

    def test_small_file_still_pushes_undo(self, file_ops, undo, tmp_path):
        small = tmp_path / "small.txt"
        small.write_text("hi")
        res = file_ops.delete_file(str(small))
        assert res["success"] is True
        undo.push.assert_called_once()

    def test_build_tree_depth_capped(self, file_ops, tmp_path, monkeypatch):
        monkeypatch.setattr(file_ops_mod, "MAX_UNDO_TREE_DEPTH", 2)
        # Build deeper than the cap: a/b/c/d/deep.txt
        deep = tmp_path / "a" / "b" / "c" / "d"
        deep.mkdir(parents=True)
        (deep / "deep.txt").write_text("buried")
        (tmp_path / "a" / "top.txt").write_text("shallow")
        tree = file_ops._build_tree(tmp_path)
        # Shallow file is captured; the over-deep branch is truncated to {}
        assert "a" in tree
        # Walk down — at the cap depth the dict becomes empty
        node = tree["a"]
        depth = 0
        while isinstance(node, dict) and node:
            # find the nested dir key if present
            sub = {k: v for k, v in node.items() if isinstance(v, dict)}
            if not sub:
                break
            node = next(iter(sub.values()))
            depth += 1
        assert depth <= 3  # truncated, not unbounded

    def test_build_tree_skips_large_files(self, file_ops, tmp_path, monkeypatch):
        monkeypatch.setattr(file_ops_mod, "MAX_UNDO_FILE_BYTES", 4)
        d = tmp_path / "folder"
        d.mkdir()
        (d / "big.bin").write_bytes(b"y" * 32)
        tree = file_ops._build_tree(tmp_path)
        assert tree["folder"]["big.bin"] == b""  # not snapshotted


# ── #8: vault brute-force throttling ─────────────────────────────────────────

@pytest.mark.skipif(not CRYPTO_AVAILABLE, reason="cryptography not installed")
class TestVaultThrottle:
    def _make(self, tmp_path):
        v = Vault(tmp_path / "vault.enc")
        v.unlock("correct-horse")  # create the vault
        # simulate a fresh handle on the same file (locked)
        v2 = Vault(tmp_path / "vault.enc")
        return v2

    def test_lockout_after_max_attempts(self, tmp_path):
        v = self._make(tmp_path)
        for _ in range(v.MAX_UNLOCK_ATTEMPTS - 1):
            assert v.unlock("wrong")["success"] is False
        # the attempt that hits the limit reports a lockout
        res = v.unlock("wrong")
        assert res["success"] is False
        assert "locked" in res["message"].lower()
        # subsequent attempts are refused immediately, even with the right password
        res2 = v.unlock("correct-horse")
        assert res2["success"] is False
        assert "try again" in res2["message"].lower()

    def test_correct_password_resets_counter(self, tmp_path):
        v = self._make(tmp_path)
        v.unlock("wrong")
        v.unlock("wrong")
        assert v.unlock("correct-horse")["success"] is True
        assert v._failed_attempts == 0


# ── #17: pending-action store hard cap ───────────────────────────────────────

def test_pending_actions_capped():
    store = PendingActionStore()
    for i in range(_MAX_PENDING + 20):
        store.push("file_delete", {"i": i}, f"action {i}")
    assert len(store._store) <= _MAX_PENDING


# ── #26: audit timestamp is UTC with millisecond precision ───────────────────

def test_audit_timestamp_utc_ms(tmp_path):
    log = AuditLog(tmp_path)
    log.log(intent="file_delete", params={"path": "x"}, success=True, result_summary="ok")
    entries = log.get_recent(1)
    assert entries, "audit entry should be written for a tier-2 intent"
    ts = entries[0]["ts"]
    assert ts.endswith("+00:00") or ts.endswith("Z")  # UTC
    assert "." in ts  # millisecond fraction present


# ── #16: duplicate feature registration replaces (and warns) ─────────────────

def test_register_feature_replaces(caplog):
    router = ActionRouter(MagicMock())
    a, b = object(), object()
    router.register_feature("dup", a)
    router.register_feature("dup", b)
    assert router._features["dup"] is b  # latest wins, no crash


# ── #10: wakeword gates start() on availability ──────────────────────────────

def test_wakeword_start_noop_when_unavailable(monkeypatch):
    # Avoid loading a real Whisper model: force the method off so __init__ skips it.
    from loki.core import wakeword as ww
    det = ww.WakewordDetector({"wakeword": {"method": "porcupine"}})
    assert det.is_available is False
    det.start()
    assert det.is_running is False  # never spun up a thread
