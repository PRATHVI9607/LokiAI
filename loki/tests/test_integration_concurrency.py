"""
Integration + concurrency tests (issue #7).

Integration: full intent → router → confirmation → execution paths, and the
destructive-op confirmation gate. Concurrency: thread-safety of the shared
stores (outcome log, pending actions, undo stack) and the rate limiter under
parallel load.
"""

import threading
from unittest.mock import MagicMock

import pytest

from loki.core.action_router import ActionRouter
from loki.core.pending_actions import PendingActionStore
from loki.core.undo_stack import UndoStack
from loki.core.outcome_log import OutcomeLog
from loki.features.git_helper import GitHelper


# ── Integration: destructive-op confirmation gate ────────────────────────────

class TestConfirmationFlow:
    def _router_with_files(self):
        router = ActionRouter(MagicMock())
        fake_files = MagicMock()
        fake_files.delete_file.return_value = {"success": True, "message": "deleted"}
        router.register_action("file_ops", fake_files)
        return router, fake_files

    def test_destructive_intent_requires_confirmation(self):
        router, fake_files = self._router_with_files()
        res = router.route_intent({"intent": "file_delete", "params": {"path": "x.txt"}})
        assert res.get("pending") is True
        assert "token" in res
        fake_files.delete_file.assert_not_called()  # NOT executed yet

    def test_confirm_executes_pending(self):
        router, fake_files = self._router_with_files()
        pending = router.route_intent({"intent": "file_delete", "params": {"path": "x.txt"}})
        token = pending["token"]
        done = router.route_intent({"intent": "confirm_action", "params": {"token": token}})
        assert done["success"] is True
        fake_files.delete_file.assert_called_once()

    def test_cancel_drops_pending(self):
        router, fake_files = self._router_with_files()
        router.route_intent({"intent": "file_delete", "params": {"path": "x.txt"}})
        res = router.route_intent({"intent": "cancel_action", "params": {}})
        assert res["success"] is True
        fake_files.delete_file.assert_not_called()

    def test_git_push_is_gated(self):
        router = ActionRouter(MagicMock())
        gh = MagicMock()
        gh.push.return_value = {"success": True, "message": "pushed"}
        router.register_feature("git_helper", gh)
        res = router.route_intent({"intent": "git_push", "params": {}})
        assert res.get("pending") is True
        gh.push.assert_not_called()


# ── Integration: git SSH-remote classification (issue #8) ────────────────────

class TestGitRemoteKind:
    def test_ssh_forms(self):
        assert GitHelper._remote_kind("git@github.com:user/repo.git") == "ssh"
        assert GitHelper._remote_kind("ssh://git@host/repo.git") == "ssh"

    def test_https_form(self):
        assert GitHelper._remote_kind("https://github.com/user/repo.git") == "https"

    def test_blank(self):
        assert GitHelper._remote_kind("") == "other"


# ── Concurrency: shared stores are thread-safe ───────────────────────────────

def _run_parallel(fn, n_threads=10, per_thread=50):
    threads = [threading.Thread(target=fn, args=(per_thread,)) for _ in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=10)


class TestConcurrency:
    def test_outcome_log_parallel_writes(self, tmp_path):
        log = OutcomeLog(tmp_path)

        def worker(n):
            for i in range(n):
                log.log(f"q{i}", intent="chat", success=True, provider="ollama")

        _run_parallel(worker, n_threads=8, per_thread=25)
        # 8 * 25 = 200 rows, all well-formed (no torn JSON lines)
        rows = log._all()
        assert len(rows) == 200

    def test_pending_store_parallel(self):
        store = PendingActionStore()

        def worker(n):
            for i in range(n):
                a = store.push("file_delete", {"i": i}, "d")
                store.pop(a.token)

        _run_parallel(worker, n_threads=8, per_thread=25)
        # store stays bounded and consistent (no exceptions, capped)
        assert len(store._store) <= 50

    def test_undo_stack_parallel(self):
        stack = UndoStack(max_depth=25)

        def worker(n):
            for i in range(n):
                stack.push("noop", {}, "x", undo_fn=lambda s: None)

        _run_parallel(worker, n_threads=8, per_thread=25)
        assert len(stack) <= 25  # depth cap holds under concurrency

    def test_rate_limiter_thread_safe(self):
        from loki.ui.server import RateLimiter
        rl = RateLimiter(max_events=1000, window_sec=60.0)
        allowed = []
        lock = threading.Lock()

        def worker(n):
            local = sum(1 for _ in range(n) if rl.allow())
            with lock:
                allowed.append(local)

        _run_parallel(worker, n_threads=10, per_thread=200)
        # Never hand out more than the cap, even with 2000 concurrent attempts
        assert sum(allowed) <= 1000
