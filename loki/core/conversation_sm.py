"""
ConversationStateMachine — replaces the monolithic ConversationManager.

States:
  IDLE      → conversation not active; wakeword owns mic
  LISTENING → waiting for user utterance; inactivity timer armed
  THINKING  → LLM + action router running on worker thread; timer cancelled
  SPEAKING  → TTS playing a response; timer cancelled
  ENDING    → farewell spoken on timeout; waiting for TTS to drain before tear-down

Transition rules:
  IDLE      → LISTENING  : start_conversation()
  LISTENING → THINKING   : process_input(text)
  THINKING  → SPEAKING   : response ready (inside worker thread)
  SPEAKING  → LISTENING  : on_tts_done() while still active
  SPEAKING  → IDLE       : on_tts_done() after end_conversation()
  LISTENING → ENDING     : _on_timeout() → speak farewell
  ENDING    → IDLE       : on_tts_done() when _state==ENDING

All state transitions are protected by _lock; callbacks fire outside the lock.
"""

import logging
import random
import threading
from enum import Enum, auto
from typing import Callable, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from loki.core.brain import LokiBrain
    from loki.core.tts import LokiTTS
    from loki.core.action_router import ActionRouter
    from loki.core.audit import AuditLog
    from loki.core.outcome_log import OutcomeLog

logger = logging.getLogger(__name__)

DISMISSALS = [
    "Farewell. Try not to cause chaos without me.",
    "Until next time. Don't touch anything important.",
    "Gone, but never truly absent.",
]


class ConvState(Enum):
    IDLE      = auto()
    LISTENING = auto()
    THINKING  = auto()
    SPEAKING  = auto()
    ENDING    = auto()


class ConversationStateMachine:
    """Manages conversation state and drives LLM/action/TTS flow."""

    def __init__(
        self,
        config: dict,
        server,
        tts: "LokiTTS",
        brain: "LokiBrain",
        router: "ActionRouter",
        audit_log: Optional["AuditLog"] = None,
        outcome_log: Optional["OutcomeLog"] = None,
    ):
        self._cfg = config
        self._server = server
        self._tts = tts
        self._brain = brain
        self._router = router
        self._audit = audit_log
        self._outcomes = outcome_log
        self._last_outcome_id: Optional[str] = None  # for feedback attachment

        self._state = ConvState.IDLE
        self._lock = threading.Lock()
        self._timeout_sec = config.get("ui", {}).get("conversation_timeout_seconds", 30)
        self._timeout_handle: Optional[threading.Timer] = None
        self._process_thread: Optional[threading.Thread] = None

        # Outbound callbacks (set by LokiApplication)
        self.on_ready_for_next: Optional[Callable] = None   # mic back to listening
        self.on_ended: Optional[Callable] = None            # mic back to wakeword

    # ── Properties ──────────────────────────────────────────────────────

    @property
    def state(self) -> ConvState:
        return self._state

    @property
    def is_active(self) -> bool:
        return self._state != ConvState.IDLE

    # ── Conversation lifecycle ───────────────────────────────────────────

    def start_conversation(self) -> None:
        with self._lock:
            if self._state != ConvState.IDLE:
                # Already active — just re-arm the timeout if we're listening
                if self._state == ConvState.LISTENING:
                    self._arm_timeout()
                return
            self._state = ConvState.LISTENING
        self._server.show_window()
        self._server.set_status("listening")
        self._arm_timeout()
        logger.info("● conversation started [LISTENING]")

    def barge_in(self) -> None:
        """Interrupt Loki mid-sentence — cut TTS and return to listening.
        Triggered by the UI stop button or by a new message arriving while speaking."""
        self._tts.stop()
        with self._lock:
            if self._state == ConvState.SPEAKING:
                self._state = ConvState.LISTENING
        self._server.set_status("listening")
        logger.info("✋ barge-in — speech interrupted [LISTENING]")

    def process_input(self, text: str) -> None:
        if not text or not text.strip():
            return
        with self._lock:
            # Barge-in: a new message while Loki is speaking interrupts it.
            if self._state == ConvState.SPEAKING:
                interrupt = True
            elif self._state not in (ConvState.LISTENING, ConvState.IDLE):
                logger.warning("process_input called in state %s — ignoring", self._state)
                return
            else:
                interrupt = False
            self._state = ConvState.THINKING
        if interrupt:
            self._tts.stop()  # silence the current/queued speech before answering anew
        self._cancel_timeout()
        self._server.add_user_message(text)
        self._server.set_status("thinking")
        self._server.clear_transcript()
        logger.info("🧠 thinking… [THINKING]")

        # Run LLM + action on a worker thread so the voice pipeline stays responsive
        self._process_thread = threading.Thread(
            target=self._process_worker,
            args=(text,),
            daemon=True,
            name="loki-process",
        )
        self._process_thread.start()

    def end_conversation(self) -> None:
        """Immediately end (browser close, mute, etc.) — no farewell."""
        with self._lock:
            self._state = ConvState.IDLE
        self._cancel_timeout()
        self._server.set_status("idle")
        self._server.hide_window()
        logger.info("○ conversation ended [IDLE]")
        if self.on_ended:
            self.on_ended()

    def on_tts_done(self) -> None:
        """Called by LokiApplication when TTS queue drains completely."""
        with self._lock:
            if self._state == ConvState.ENDING:
                self._state = ConvState.IDLE
                do_end = True
            elif self._state == ConvState.SPEAKING:
                self._state = ConvState.LISTENING
                do_end = False
            else:
                return

        if do_end:
            self._server.set_status("idle")
            self._server.hide_window()
            logger.info("○ farewell done [IDLE] — back to wakeword")
            if self.on_ended:
                self.on_ended()
        else:
            self._server.set_status("listening")
            self._arm_timeout()
            logger.info("● ready for next [LISTENING]")
            if self.on_ready_for_next:
                self.on_ready_for_next()

    # ── Internal ────────────────────────────────────────────────────────

    def _on_timeout(self) -> None:
        with self._lock:
            if self._state != ConvState.LISTENING:
                return
            self._state = ConvState.ENDING
        farewell = random.choice(DISMISSALS)
        self._server.add_loki_message(farewell)
        self._server.set_status("speaking")
        self._tts.speak(farewell)
        logger.info("⏱ timeout — saying farewell [ENDING]")

    def _arm_timeout(self) -> None:
        self._cancel_timeout()
        self._timeout_handle = threading.Timer(self._timeout_sec, self._on_timeout)
        self._timeout_handle.daemon = True
        self._timeout_handle.start()

    def _cancel_timeout(self) -> None:
        if self._timeout_handle:
            self._timeout_handle.cancel()
            self._timeout_handle = None

    # ── Worker thread (LLM + action) ─────────────────────────────────────

    def _process_worker(self, text: str) -> None:
        import time as _time
        _start = _time.time()
        self._last_outcome_id = None  # fresh per turn — avoids stale feedback attribution
        try:
            response = ""
            for chunk in self._brain.ask(text):
                response += chunk

            if not response.strip():
                response = "Hmm. That query produced nothing of substance. Try again."

            # Snapshot signals for the outcome logger (latency, which provider answered,
            # whether the deterministic fast-path or the LLM produced this).
            provider = getattr(self._brain, "last_provider", "unknown")
            self._pending_outcome = {
                "transcript": text,
                "latency_ms": int((_time.time() - _start) * 1000),
                "provider": provider,
                "source": "fast_path" if provider == "fast_path" else "llm",
            }

            intent = self._brain.parse_intent(response)
            if intent and intent.get("intent") and intent["intent"] != "chat":
                self._handle_intent(intent)
            else:
                self._record_outcome(intent="chat", params={}, success=True, response=response)
                self._emit_response(response, outcome_id=self._last_outcome_id)

        except Exception as e:
            logger.error("Process worker error: %s", e, exc_info=True)
            self._record_outcome(intent="error", params={}, success=False, response=str(e)[:200])
            self._emit_response("Something went awry. Even gods have bad days.")

    def _record_outcome(self, intent: str, params: dict, success: bool, response: str = "") -> None:
        """Passive training-data capture — never alters behaviour. Safe no-op if unset."""
        if not self._outcomes:
            return
        p = getattr(self, "_pending_outcome", None) or {}
        try:
            self._last_outcome_id = self._outcomes.log(
                transcript=p.get("transcript", ""),
                intent=intent,
                params=params,
                success=success,
                latency_ms=p.get("latency_ms", 0),
                provider=p.get("provider", "unknown"),
                source=p.get("source", "llm"),
                response=response,
            )
        except Exception as e:
            logger.debug("outcome log skipped: %s", e)

    def _handle_intent(self, intent: Dict) -> None:
        intent_name = intent.get("intent", "")
        loki_msg = intent.get("message", "")

        # Route FIRST — never speak an optimistic promise before we know the
        # action is real and succeeded. (The LLM sometimes invents intents like
        # "weather_fetch" that don't exist and promises results it can't deliver.)
        self._server.set_status("thinking")
        result = self._router.route_intent(intent)
        result_msg = result.get("message", "")

        if self._audit:
            self._audit.log(
                intent=intent_name,
                params=intent.get("params", {}),
                success=result.get("success", False),
                result_summary=result_msg,
            )

        # Passive training-data capture (RL step #1) — every intent outcome.
        self._record_outcome(
            intent=intent_name,
            params=intent.get("params", {}),
            success=result.get("success", False),
            response=result_msg,
        )

        # Pending confirmation — speak the confirm prompt, wait for the user
        if result.get("pending"):
            self._emit_response(result_msg, speak=True)
            with self._lock:
                self._state = ConvState.LISTENING
            self._server.set_status("listening")
            self._arm_timeout()
            if self.on_ready_for_next:
                self.on_ready_for_next()
            return

        # Hallucinated / unsupported intent — answer honestly instead of
        # speaking the LLM's misleading promise.
        if not result.get("success") and result_msg.lower().startswith("unknown intent"):
            logger.warning(f"LLM emitted unsupported intent '{intent_name}' — answering as chat")
            self._emit_response("That's not in my repertoire. Ask me something else.", speak=True)
            return

        if result.get("success"):
            # Speak the conversational ack (if any), then the concrete result.
            # The thumbs 👍/👎 attaches to the final/concrete message of the turn.
            has_result = bool(result_msg and result_msg != loki_msg)
            if loki_msg:
                self._emit_response(loki_msg, speak=True,
                                    outcome_id=None if has_result else self._last_outcome_id)
            if has_result:
                self._emit_response(result_msg, speak=True, outcome_id=self._last_outcome_id)
        else:
            self._emit_response(result_msg or "That operation failed.", speak=True,
                                outcome_id=self._last_outcome_id)

    def _emit_response(self, text: str, speak: bool = True, outcome_id: Optional[str] = None) -> None:
        provider = getattr(self._brain, "last_provider", None)
        self._server.add_loki_message(text, outcome_id=outcome_id, provider=provider)
        if speak and text:
            with self._lock:
                self._state = ConvState.SPEAKING
            self._server.set_status("speaking")
            logger.info(f"💬 Loki: \"{text[:80]}{'…' if len(text) > 80 else ''}\" [SPEAKING]")
            self._tts.speak(text)
        else:
            # No TTS — transition back to LISTENING directly
            with self._lock:
                if self._state == ConvState.THINKING:
                    self._state = ConvState.LISTENING
            self._server.set_status("listening")
            self._arm_timeout()
            if self.on_ready_for_next:
                self.on_ready_for_next()
