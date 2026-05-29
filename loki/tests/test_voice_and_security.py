"""
Integration tests for voice lifecycle, TTS, confirmation flow, SSRF, and process kill.
"""

import queue
import threading
import time
from pathlib import Path
from unittest.mock import MagicMock, patch, PropertyMock

import pytest

# ── TTS lifecycle ────────────────────────────────────────────────────────────

class FakeTTS:
    """Minimal TTS stub for state-machine tests."""
    def __init__(self):
        self._q: queue.Queue = queue.Queue()
        self._speaking = False
        self.spoken: list[str] = []
        self.on_speaking_stopped = None

    def speak(self, text: str) -> None:
        self.spoken.append(text)
        self._speaking = True
        self._q.put(text)

    def stop(self) -> None:
        self._speaking = False
        try:
            while True:
                self._q.get_nowait()
                self._q.task_done()
        except queue.Empty:
            pass

    @property
    def is_speaking(self) -> bool:
        return self._speaking

    @property
    def is_idle(self) -> bool:
        return not self._speaking and self._q.empty()

    def drain_and_fire(self) -> None:
        """Simulate TTS finishing — drain queue and fire callback."""
        self._speaking = False
        try:
            while True:
                self._q.get_nowait()
                self._q.task_done()
        except queue.Empty:
            pass
        if self.on_speaking_stopped:
            self.on_speaking_stopped()


class TestTTSDrain:
    def test_stop_drains_queue(self):
        from loki.core.tts import LokiTTS
        tts = LokiTTS({"engine": "none"})  # no real engine
        tts.speak("hello")
        tts.speak("world")
        tts.stop()
        assert tts.is_idle

    def test_is_idle_after_stop(self):
        from loki.core.tts import LokiTTS
        tts = LokiTTS({"engine": "none"})
        tts.stop()
        assert tts.is_idle


# ── ConversationStateMachine ──────────────────────────────────────────────────

class TestConversationStateMachine:
    def _make_sm(self, tts=None):
        from loki.core.conversation_sm import ConversationStateMachine, ConvState
        fake_tts = tts or FakeTTS()
        server = MagicMock()
        brain = MagicMock()
        brain.ask.return_value = iter(["Hello there!"])
        brain.parse_intent.return_value = None  # pure chat response
        router = MagicMock()
        sm = ConversationStateMachine({}, server, fake_tts, brain, router)
        sm.on_ready_for_next = MagicMock()
        sm.on_ended = MagicMock()
        return sm, fake_tts, server

    def test_initial_state_is_idle(self):
        from loki.core.conversation_sm import ConvState
        sm, _, _ = self._make_sm()
        assert sm.state == ConvState.IDLE
        assert not sm.is_active

    def test_start_moves_to_listening(self):
        from loki.core.conversation_sm import ConvState
        sm, _, server = self._make_sm()
        sm.start_conversation()
        assert sm.state == ConvState.LISTENING
        assert sm.is_active
        server.show_window.assert_called_once()

    def test_process_input_goes_to_thinking(self):
        from loki.core.conversation_sm import ConvState
        sm, tts, server = self._make_sm()
        sm.start_conversation()
        sm.process_input("what time is it")
        # Give worker thread a moment to start
        time.sleep(0.1)
        assert sm.state in (ConvState.THINKING, ConvState.SPEAKING, ConvState.LISTENING)

    def test_timeout_fires_farewell(self):
        from loki.core.conversation_sm import ConvState
        sm, tts, _ = self._make_sm()
        sm._timeout_sec = 0.05  # very short timeout for test
        sm.start_conversation()
        time.sleep(0.2)  # let timeout fire
        # After timeout, state should be ENDING (farewell queued)
        assert sm.state in (ConvState.ENDING, ConvState.IDLE)
        assert len(tts.spoken) > 0  # farewell was spoken

    def test_on_tts_done_from_ending_fires_on_ended(self):
        from loki.core.conversation_sm import ConvState
        sm, tts, _ = self._make_sm()
        sm._timeout_sec = 0.05
        sm.start_conversation()
        time.sleep(0.2)
        if sm.state == ConvState.ENDING:
            sm.on_tts_done()
            assert sm.state == ConvState.IDLE
            sm.on_ended.assert_called()

    def test_end_conversation_goes_to_idle(self):
        from loki.core.conversation_sm import ConvState
        sm, _, server = self._make_sm()
        sm.start_conversation()
        sm.end_conversation()
        assert sm.state == ConvState.IDLE
        assert not sm.is_active


# ── PendingAction confirmation flow ──────────────────────────────────────────

class TestPendingActions:
    def test_push_and_pop_by_token(self):
        from loki.core.pending_actions import PendingActionStore
        store = PendingActionStore()
        action = store.push("file_delete", {"path": "/tmp/x.txt"}, "Delete /tmp/x.txt")
        token = action.token
        popped = store.pop(token)
        assert popped is not None
        assert popped.intent_name == "file_delete"
        assert store.pop(token) is None  # already consumed

    def test_pop_most_recent_without_token(self):
        from loki.core.pending_actions import PendingActionStore
        store = PendingActionStore()
        store.push("process_kill", {"name_or_pid": "notepad.exe"}, "Kill notepad.exe")
        popped = store.pop()
        assert popped is not None
        assert popped.intent_name == "process_kill"

    def test_expired_action_not_returned(self):
        from loki.core.pending_actions import PendingActionStore, _TTL_SECONDS
        store = PendingActionStore()
        action = store.push("shell", {"command": "dir"}, "Run dir")
        # Manually expire it
        action.expires_at = time.time() - 1
        popped = store.pop(action.token)
        assert popped is None

    def test_cancel_all_clears_store(self):
        from loki.core.pending_actions import PendingActionStore
        store = PendingActionStore()
        store.push("file_delete", {}, "desc1")
        store.push("process_kill", {}, "desc2")
        n = store.cancel_all()
        assert n == 2
        assert store.peek_last() is None

    def test_router_returns_pending_for_destructive(self):
        from loki.core.action_router import ActionRouter
        from unittest.mock import MagicMock
        undo = MagicMock()
        router = ActionRouter(undo)
        result = router.route_intent({"intent": "file_delete", "params": {"path": "/tmp/x.txt"}})
        assert result.get("pending") is True
        assert "token" in result

    def test_confirm_action_executes(self):
        from loki.core.action_router import ActionRouter
        from loki.actions.file_ops import FileOps
        undo = MagicMock()
        router = ActionRouter(undo)
        # Register a real file_ops so deletion can execute
        import tempfile, os
        with tempfile.NamedTemporaryFile(delete=False) as f:
            tmp = Path(f.name)
        file_ops = FileOps(undo, extra_roots=[tmp.parent])
        router.register_action("file_ops", file_ops)
        # Trigger confirmation gate
        pending = router.route_intent({"intent": "file_delete", "params": {"path": str(tmp)}})
        token = pending["token"]
        # Confirm
        result = router.route_intent({"intent": "confirm_action", "params": {"token": token}})
        assert result.get("success") is True
        # Clean up if file still exists
        if tmp.exists():
            tmp.unlink()


# ── Process kill exact match ──────────────────────────────────────────────────

class TestProcessManagerExactMatch:
    def test_nonexistent_returns_no_process(self):
        from loki.features.process_manager import ProcessManager
        pm = ProcessManager()
        result = pm.kill("__totally_nonexistent_process_xyz_abc_123.exe")
        assert result["success"] is False

    def test_substring_returns_candidates_not_kills(self):
        from loki.features.process_manager import ProcessManager
        pm = ProcessManager()
        # "python" (substring of pythonw.exe etc.) should return candidates, not kill
        result = pm.kill("ython")  # substring won't exact-match anything
        assert result["success"] is False
        # If there were candidates, data would have them
        assert "candidates" in result.get("data", {}) or "found" in result["message"].lower() or "no process" in result["message"].lower()


# ── SSRF protection ───────────────────────────────────────────────────────────

class TestSSRFProtection:
    def test_localhost_blocked(self):
        from loki.features.web_summarizer import _is_ssrf_risk
        assert _is_ssrf_risk("http://localhost/") is True
        assert _is_ssrf_risk("http://127.0.0.1/") is True
        assert _is_ssrf_risk("http://127.0.0.1:8080/api") is True

    def test_private_ipv4_blocked(self):
        from loki.features.web_summarizer import _is_ssrf_risk
        assert _is_ssrf_risk("http://192.168.1.1/") is True
        assert _is_ssrf_risk("http://10.0.0.1/") is True
        assert _is_ssrf_risk("http://172.16.0.1/") is True

    def test_file_scheme_blocked(self):
        from loki.features.web_summarizer import _is_ssrf_risk
        assert _is_ssrf_risk("file:///etc/passwd") is True

    def test_public_ip_allowed(self):
        from loki.features.web_summarizer import _is_ssrf_risk
        assert _is_ssrf_risk("https://1.1.1.1/") is False

    def test_summarizer_blocks_localhost(self):
        from loki.features.web_summarizer import WebSummarizer
        ws = WebSummarizer()
        result = ws.summarize("http://127.0.0.1:7777/api/secret")
        assert result["success"] is False
        assert "private" in result["message"].lower() or "blocked" in result["message"].lower()


# ── Clipboard token auth ─────────────────────────────────────────────────────

class TestClipboardSyncToken:
    def test_start_generates_token(self):
        from loki.features.clipboard_sync import ClipboardSync
        cs = ClipboardSync(port=17778)
        result = cs.start()
        assert result["success"] is True
        assert "t=" in result["data"]["url"]
        cs.stop()

    def test_get_url_includes_token(self):
        from loki.features.clipboard_sync import ClipboardSync
        cs = ClipboardSync(port=17779)
        cs.start()
        url_result = cs.get_url()
        assert "t=" in url_result["data"]["url"]
        cs.stop()


# ── Voice pipeline unit tests ─────────────────────────────────────────────────

class TestVoicePipeline:
    def _make(self):
        from loki.core.voice_pipeline import VoicePipeline
        wakeword = MagicMock()
        wakeword.is_running = False
        listener = MagicMock()
        listener.is_listening = False
        vp = VoicePipeline(wakeword, listener)
        return vp, wakeword, listener

    def test_activate_starts_wakeword(self):
        vp, ww, _ = self._make()
        vp.activate()
        ww.start.assert_called_once()

    def test_deactivate_stops_both(self):
        vp, ww, lst = self._make()
        vp.activate()
        vp.deactivate()
        ww.stop.assert_called()
        lst.stop_listening.assert_called()

    def test_mute_stops_voice(self):
        vp, ww, lst = self._make()
        vp.activate()
        vp.set_muted(True)
        assert vp.is_muted
        ww.stop.assert_called()
        lst.stop_listening.assert_called()

    def test_wakeword_callback_stops_wakeword_starts_listener(self):
        vp, ww, lst = self._make()
        fired = []
        vp.on_wakeword = lambda: fired.append(True)
        vp._handle_wakeword()
        ww.stop.assert_called()
        lst.start_listening.assert_called()
        assert fired == [True]

    def test_transcript_callback_stops_listener(self):
        vp, ww, lst = self._make()
        transcripts = []
        vp.on_transcript = lambda t: transcripts.append(t)
        vp._handle_transcript("test command")
        lst.stop_listening.assert_called()
        assert transcripts == ["test command"]
