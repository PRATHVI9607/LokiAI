"""
ProviderBandit — the part that makes Loki get *better* with use (RL step #2).

A contextual multi-armed bandit over LLM providers. It reads the outcome log
(the passive training data from outcome_log.py) and learns which provider gives
the best reward on THIS machine + network, then reorders which provider Loki
tries first. Falls back to the default priority order until it has data, so
behaviour is unchanged on a cold start.

reward(interaction) = success(1/0)
                    + feedback_bonus   (👍 +0.5, 👎 -0.5)
                    - latency_penalty  (latency_ms / 12000, capped at 0.5)

Selection: epsilon-greedy. With prob ε it explores (random order) so a provider
that's currently behind still gets sampled and can recover; otherwise it exploits
(best mean reward first). Unseen providers get an optimistic prior so they're
tried at least a few times before being judged.

This is intentionally simple and dependency-free — no torch, no training loop.
It runs in microseconds and improves every time you use Loki.
"""

import logging
import random
import threading
import time
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

_OPTIMISTIC_PRIOR = 0.8     # reward assumed for a provider with no/low data
_MIN_SAMPLES = 3            # below this, keep using the optimistic prior
_REFRESH_SECONDS = 30       # how often to re-read the outcome log
_RECENT_WINDOW = 400        # only learn from the last N interactions (adapts to drift)


def reward(row: dict) -> float:
    """Scalar reward for one logged interaction."""
    r = 1.0 if row.get("success") else 0.0
    fb = row.get("feedback")
    if fb == "up":
        r += 0.5
    elif fb == "down":
        r -= 0.5
    r -= min(0.5, row.get("latency_ms", 0) / 12000.0)
    return r


def _family(provider: str) -> str:
    """Normalize 'openrouter:google/gemma' → 'openrouter'."""
    return (provider or "unknown").split(":", 1)[0]


class ProviderBandit:
    def __init__(self, outcome_log, epsilon: float = 0.15, enabled: bool = True):
        self._log = outcome_log
        self._epsilon = epsilon
        self._enabled = enabled
        self._lock = threading.Lock()
        self._stats: Dict[str, Dict[str, float]] = {}  # family -> {n, mean}
        self._last_refresh = 0.0

    # ── learning ─────────────────────────────────────────────────────────

    def _refresh(self) -> None:
        now = time.time()
        if now - self._last_refresh < _REFRESH_SECONDS and self._stats:
            return
        self._last_refresh = now
        try:
            rows = self._log._all()[-_RECENT_WINDOW:] if self._log else []
        except Exception:
            rows = []
        agg: Dict[str, Dict[str, float]] = {}
        for row in rows:
            fam = _family(row.get("provider", "unknown"))
            if fam in ("fast_path", "none", "unknown"):
                continue  # fast_path isn't an LLM choice; skip non-providers
            a = agg.setdefault(fam, {"n": 0.0, "sum": 0.0})
            a["n"] += 1
            a["sum"] += reward(row)
        stats = {f: {"n": a["n"], "mean": (a["sum"] / a["n"]) if a["n"] else 0.0}
                 for f, a in agg.items()}
        with self._lock:
            self._stats = stats

    def _score(self, family: str) -> float:
        """Estimated reward — optimistic until we have enough samples."""
        s = self._stats.get(family)
        if not s or s["n"] < _MIN_SAMPLES:
            return _OPTIMISTIC_PRIOR
        return s["mean"]

    # ── selection ────────────────────────────────────────────────────────

    def rank(self, candidates: List[str]) -> List[str]:
        """Reorder provider candidates best-first. Stable/no-op when disabled."""
        if not self._enabled or len(candidates) < 2:
            return list(candidates)
        self._refresh()
        # Explore: occasionally try a random order so laggards keep getting sampled.
        if random.random() < self._epsilon:
            order = list(candidates)
            random.shuffle(order)
            logger.debug("bandit: exploring (random order)")
            return order
        # Exploit: highest estimated reward first; ties keep original priority.
        ranked = sorted(
            enumerate(candidates),
            key=lambda ic: (-self._score(_family(ic[1])), ic[0]),
        )
        return [c for _, c in ranked]

    def snapshot(self) -> Dict[str, Dict[str, float]]:
        """Current learned estimates — for the stats dashboard."""
        self._refresh()
        with self._lock:
            return {
                f: {"samples": int(v["n"]), "avg_reward": round(v["mean"], 3)}
                for f, v in self._stats.items()
            }
