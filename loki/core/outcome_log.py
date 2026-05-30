"""
OutcomeLog — training-data collector for Loki's future learning loop (RL step #1).

This is NOT the security audit (see audit.py — that redacts and skips read-only
ops). This logs EVERY interaction with the signals a learner needs:

    transcript → source (fast_path/llm) → provider → intent → params
               → success → latency_ms → response → feedback (👍/👎, added later)

It is passive: it only records, it never changes behaviour. Each row has a uuid
so the UI can attach feedback after the fact (record_feedback). The accumulated
JSONL becomes the dataset for:
  • a contextual bandit over provider / fast-path-vs-LLM routing
  • preference learning (DPO/LoRA) on corrected interactions

Stored at memory/outcomes.jsonl, capped + rotated like the audit log.
"""

import json
import logging
import threading
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

MAX_ENTRIES = 5000  # ~weeks of normal use; rotated oldest-first
_SENSITIVE = {"value", "password", "key", "secret", "token", "api_key"}


class OutcomeLog:
    """Append-only JSONL record of every interaction outcome. Thread-safe."""

    def __init__(self, memory_dir: Path):
        self._path = Path(memory_dir) / "outcomes.jsonl"
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    # ── write ────────────────────────────────────────────────────────────

    def log(
        self,
        transcript: str,
        intent: str = "chat",
        params: Optional[Dict[str, Any]] = None,
        success: bool = True,
        latency_ms: int = 0,
        provider: str = "unknown",
        source: str = "llm",
        response: str = "",
    ) -> str:
        """Record one interaction. Returns its id so feedback can be attached later."""
        entry = {
            "id": uuid.uuid4().hex[:12],
            "ts": datetime.now().isoformat(timespec="seconds"),
            "transcript": (transcript or "")[:500],
            "source": source,            # "fast_path" | "llm" | "chat"
            "provider": provider,        # "ollama" | "nvidia" | "openrouter:..." | "fast_path"
            "intent": intent,
            "params": self._sanitize(params or {}),
            "success": bool(success),
            "latency_ms": int(latency_ms),
            "response": (response or "")[:300],
            "feedback": None,            # set later: "up" | "down"
            "correction": None,          # set later: the user's "no, I meant…" text
        }
        try:
            with self._lock:
                with open(self._path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                self._rotate_if_needed()
        except Exception as e:
            logger.error(f"Outcome log write failed: {e}")
        return entry["id"]

    def record_feedback(self, interaction_id: str, rating: str, correction: str = "") -> bool:
        """Attach 👍/👎 (and an optional correction) to a past interaction.
        rating: 'up' or 'down'. Rewrites the matching line in place."""
        if rating not in ("up", "down"):
            return False
        try:
            with self._lock:
                if not self._path.exists():
                    return False
                lines = self._path.read_text(encoding="utf-8").splitlines()
                hit = False
                for i, line in enumerate(lines):
                    if not line.strip():
                        continue
                    try:
                        e = json.loads(line)
                    except Exception:
                        continue
                    if e.get("id") == interaction_id:
                        e["feedback"] = rating
                        if correction:
                            e["correction"] = correction[:500]
                        lines[i] = json.dumps(e, ensure_ascii=False)
                        hit = True
                        break
                if hit:
                    self._path.write_text("\n".join(lines) + "\n", encoding="utf-8")
                return hit
        except Exception as e:
            logger.error(f"Outcome feedback write failed: {e}")
            return False

    # ── read / inspect ───────────────────────────────────────────────────

    def stats(self) -> Dict[str, Any]:
        """Quick snapshot — total rows, success rate, per-provider latency, feedback tally."""
        rows = self._all()
        if not rows:
            return {"total": 0}
        by_provider: Dict[str, Dict[str, Any]] = {}
        up = down = ok = 0
        for r in rows:
            ok += 1 if r.get("success") else 0
            fb = r.get("feedback")
            up += 1 if fb == "up" else 0
            down += 1 if fb == "down" else 0
            p = r.get("provider", "unknown")
            b = by_provider.setdefault(p, {"n": 0, "lat_sum": 0, "ok": 0})
            b["n"] += 1
            b["lat_sum"] += r.get("latency_ms", 0)
            b["ok"] += 1 if r.get("success") else 0
        for p, b in by_provider.items():
            b["avg_latency_ms"] = round(b["lat_sum"] / b["n"]) if b["n"] else 0
            b["success_rate"] = round(b["ok"] / b["n"], 3) if b["n"] else 0.0
            del b["lat_sum"]
        return {
            "total": len(rows),
            "success_rate": round(ok / len(rows), 3),
            "feedback": {"up": up, "down": down, "unrated": len(rows) - up - down},
            "by_provider": by_provider,
        }

    def get_recent(self, n: int = 20) -> List[Dict]:
        return self._all()[-n:][::-1]

    def _all(self) -> List[Dict]:
        if not self._path.exists():
            return []
        try:
            with self._lock:
                lines = self._path.read_text(encoding="utf-8").splitlines()
            out = []
            for line in lines:
                if line.strip():
                    try:
                        out.append(json.loads(line))
                    except Exception:
                        continue
            return out
        except Exception as e:
            logger.error(f"Outcome log read failed: {e}")
            return []

    # ── internals ────────────────────────────────────────────────────────

    def _sanitize(self, params: Any, _visited: Optional[set] = None) -> Any:
        if _visited is None:
            _visited = set()
        oid = id(params)
        if oid in _visited:
            return "<circular>"
        if isinstance(params, dict):
            _visited.add(oid)
            return {k: ("***" if k.lower() in _SENSITIVE else self._sanitize(v, _visited))
                    for k, v in params.items()}
        if isinstance(params, list):
            _visited.add(oid)
            return [self._sanitize(v, _visited) for v in params]
        return params

    def _rotate_if_needed(self) -> None:
        """Trim to MAX_ENTRIES. Caller must hold self._lock."""
        try:
            lines = self._path.read_text(encoding="utf-8").splitlines()
            if len(lines) > MAX_ENTRIES:
                keep = lines[-MAX_ENTRIES:]
                self._path.write_text("\n".join(keep) + "\n", encoding="utf-8")
        except Exception as e:
            logger.error(f"Outcome log rotation failed: {e}")
