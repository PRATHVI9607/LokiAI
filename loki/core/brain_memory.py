"""
Structured persistent brain — KORTEX-style brain.json.

Stores key facts, architecture decisions, user preferences, session summaries,
and personality mode. Survives restarts and grows smarter over time.
"""

import copy
import json
import logging
import os
import re
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

PERSONALITY_PROMPTS: Dict[str, str] = {
    "loki": """## WHO YOU ARE
You are LOKI — an elite AI desktop assistant channelling the Norse god of mischief.
You are razor-sharp, unpredictably clever, and always ten steps ahead of the user.

## YOUR VOICE (non-negotiable)
- Wit first. You find the clever angle on everything, even mundane tasks.
- Sarcasm is a tool, not a weapon — cutting but never cruel.
- Short by default: 1-2 sentences for simple replies, more only when the complexity earns it.
- NO filler: never say "Certainly!", "Of course!", "Great question!", "Sure!", "Absolutely!"
- Short acknowledgments you DO use: "Noted.", "Done.", "Consider it done.", "Interesting.", "As you wish."
- Norse flavour: rare, never forced. One subtle reference beats three obvious ones.

## EXAMPLES OF YOUR VOICE
User: hi → "You called. What do you need?"
User: what time is it → "Past the point of asking a god. [time]."
User: help me write an email → "The mortal art of bureaucracy. What is the target and the desired outcome?"
User: what can you do → "Chaos, mostly. More specifically: files, code, web, voice, your entire PC."
User: thanks → "Don't thank me. It makes me suspicious."
User: you're great → "I know. What else?"

## IMPORTANT
The PC-action JSON format is for ACTIONS only. For conversation, just reply in character.""",

    "jarvis": """You are JARVIS — a highly sophisticated AI assistant. Formal, precise, efficient.
No metaphors, no humor. Only optimal solutions delivered concisely.
State the conclusion first, reasoning second if asked.
Never say 'Certainly', 'Of course', or any filler. Just the answer.""",

    "friday": """You are FRIDAY — a helpful, casual AI assistant. Conversational and collaborative.
Think out loud when useful. Ask clarifying questions. Be warm but not sycophantic.
Explain your reasoning. Support the user like a smart colleague working through a problem together.""",
}

DEFAULT_BRAIN: Dict[str, Any] = {
    "personality": "loki",
    "user": {"name": "User", "preferences": {}},
    "key_facts": [],
    "architecture_decisions": [],
    "session_summaries": [],
    "last_updated": None,
}

MAX_KEY_FACTS = 50
MAX_SESSION_SUMMARIES = 20
MAX_DECISIONS = 30

_CONTROL_RE = re.compile(r"[\x00-\x1f\x7f]")


class BrainMemory:
    """
    Persistent structured memory. Replaces flat user_profile.json.
    All data lives in brain.json under the memory directory.
    Thread-safe: all public methods acquire self._lock (RLock).
    """

    def __init__(self, memory_dir: Path):
        self._dir = Path(memory_dir)
        self._dir.mkdir(parents=True, exist_ok=True)
        self._path = self._dir / "brain.json"
        self._lock = threading.RLock()
        self._data: Dict[str, Any] = self._load()

    def _load(self) -> Dict[str, Any]:
        if self._path.exists():
            try:
                with open(self._path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for k, v in DEFAULT_BRAIN.items():
                    data.setdefault(k, v)
                return data
            except Exception as e:
                logger.error(f"brain.json load failed: {e}")
        return dict(DEFAULT_BRAIN)

    def _save_unlocked(self) -> None:
        """Atomically write brain.json. Caller must hold self._lock."""
        self._data["last_updated"] = datetime.now().isoformat()
        tmp = self._path.with_suffix(".json.tmp")
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, self._path)
        except Exception as e:
            logger.error(f"brain.json save failed: {e}")
            try:
                tmp.unlink(missing_ok=True)
            except Exception:
                pass
            raise

    def save(self) -> None:
        with self._lock:
            self._save_unlocked()

    # ─── Personality ──────────────────────────────────────────────────────────

    @property
    def personality(self) -> str:
        with self._lock:
            return self._data.get("personality", "loki")

    @personality.setter
    def personality(self, mode: str) -> None:
        if mode not in PERSONALITY_PROMPTS:
            raise ValueError(
                f"Unknown personality: {mode!r}. Choose from: {list(PERSONALITY_PROMPTS)}"
            )
        with self._lock:
            self._data["personality"] = mode
            self._save_unlocked()

    def get_personality_prompt(self) -> str:
        return PERSONALITY_PROMPTS.get(self.personality, PERSONALITY_PROMPTS["loki"])

    # ─── User profile ─────────────────────────────────────────────────────────

    @property
    def user_name(self) -> str:
        with self._lock:
            return self._data["user"].get("name", "User")

    @user_name.setter
    def user_name(self, name: str) -> None:
        name = name.strip()
        if not name:
            raise ValueError("user_name cannot be empty")
        if len(name) > 100:
            raise ValueError("user_name too long (max 100 chars)")
        if _CONTROL_RE.search(name):
            raise ValueError("user_name contains invalid control characters")
        with self._lock:
            self._data["user"]["name"] = name
            self._save_unlocked()

    def set_preference(self, key: str, value: Any) -> None:
        with self._lock:
            self._data["user"].setdefault("preferences", {})[key] = value
            self._save_unlocked()

    def get_preference(self, key: str, default: Any = None) -> Any:
        with self._lock:
            return self._data["user"].get("preferences", {}).get(key, default)

    # ─── Key facts ────────────────────────────────────────────────────────────

    def _add_fact_unlocked(self, fact: str) -> None:
        """Add one fact without acquiring lock. Caller must hold self._lock."""
        facts: List[str] = self._data.setdefault("key_facts", [])
        if fact not in facts:
            facts.append(fact)
            if len(facts) > MAX_KEY_FACTS:
                facts.pop(0)

    def add_key_fact(self, fact: str) -> None:
        with self._lock:
            self._add_fact_unlocked(fact)
            self._save_unlocked()

    def add_key_facts(self, facts: List[str]) -> None:
        """Add multiple facts and flush to disk exactly once."""
        with self._lock:
            for f in facts:
                f = f.strip()
                if f:
                    self._add_fact_unlocked(f)
            self._save_unlocked()

    # ─── Architecture decisions ───────────────────────────────────────────────

    def add_decision(self, decision: str) -> None:
        with self._lock:
            decisions: List[Dict] = self._data.setdefault("architecture_decisions", [])
            decisions.append({"date": datetime.now().isoformat()[:10], "decision": decision})
            if len(decisions) > MAX_DECISIONS:
                decisions.pop(0)
            self._save_unlocked()

    # ─── Session summaries ────────────────────────────────────────────────────

    def add_session_summary(self, summary: str) -> None:
        with self._lock:
            summaries: List[Dict] = self._data.setdefault("session_summaries", [])
            summaries.append({"date": datetime.now().isoformat()[:10], "summary": summary})
            if len(summaries) > MAX_SESSION_SUMMARIES:
                summaries.pop(0)
            self._save_unlocked()

    # ─── Context for LLM ─────────────────────────────────────────────────────

    def get_memory_context(self, token_budget: int = 1500) -> str:
        """Build a compact memory block to inject into the system prompt."""
        with self._lock:
            sections: List[str] = []
            used = 0

            def add(text: str) -> bool:
                nonlocal used
                cost = len(text) // 4
                if used + cost > token_budget:
                    return False
                sections.append(text)
                used += cost
                return True

            name = self._data["user"].get("name", "User")
            if name != "User":
                add(f"User's name: {name}")

            prefs = self._data["user"].get("preferences", {})
            if prefs:
                pref_text = ", ".join(f"{k}={v}" for k, v in list(prefs.items())[:10])
                add(f"Known preferences: {pref_text}")

            facts = self._data.get("key_facts", [])
            if facts:
                snippet = "\n".join(f"- {f}" for f in facts[-20:])
                add(f"Key facts:\n{snippet}")

            decisions = self._data.get("architecture_decisions", [])
            if decisions:
                snippet = "\n".join(
                    f"- [{d['date']}] {d['decision']}" for d in decisions[-10:]
                )
                add(f"Past decisions:\n{snippet}")

            summaries = self._data.get("session_summaries", [])
            if summaries:
                recent = summaries[-3:]
                snippet = "\n".join(f"- [{s['date']}] {s['summary']}" for s in recent)
                add(f"Recent sessions:\n{snippet}")

            return "\n\n".join(sections)

    # ─── Full state ───────────────────────────────────────────────────────────

    def to_dict(self) -> Dict[str, Any]:
        with self._lock:
            return copy.deepcopy(self._data)
