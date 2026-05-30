"""
SecondBrain — Loki's personal long-term memory ("remember this" / "what did I
say about X").

"Remember that my API key rotates every 90 days."
"What did I save about the API key?"

Notes live in memory/notes.json (the source of truth). Recall is semantic when
the RAG embedder (nomic-embed-text via Ollama) is reachable — it embeds the
query and ranks notes by cosine similarity. If embeddings aren't available it
falls back to keyword overlap, so it always works.

Returns the standard {success, message, data} envelope.
"""

import json
import logging
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class SecondBrain:
    def __init__(self, memory_dir: Path, rag_engine=None):
        self._path = Path(memory_dir) / "notes.json"
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._rag = rag_engine            # optional — used only for embeddings
        self._lock = threading.Lock()
        self._notes: List[Dict[str, Any]] = self._load()

    def _load(self) -> List[Dict[str, Any]]:
        if not self._path.exists():
            return []
        try:
            return json.loads(self._path.read_text(encoding="utf-8"))
        except Exception:
            return []

    def _save(self) -> None:
        try:
            self._path.write_text(json.dumps(self._notes, ensure_ascii=False, indent=2),
                                  encoding="utf-8")
        except Exception as e:
            logger.error(f"SecondBrain save failed: {e}")

    # ── write ────────────────────────────────────────────────────────────

    def remember(self, text: str) -> Dict[str, Any]:
        text = (text or "").strip()
        if not text:
            return {"success": False, "message": "Remember what, exactly?"}
        emb = self._try_embed(text)
        note = {"id": int(time.time() * 1000), "text": text, "ts": time.time(), "embed": emb}
        with self._lock:
            self._notes.append(note)
            self._save()
        return {"success": True, "message": "Noted. I'll remember that.", "data": {"count": len(self._notes)}}

    def forget(self, query: str) -> Dict[str, Any]:
        ranked = self._rank(query, top_k=1)
        if not ranked:
            return {"success": True, "message": "Nothing matching to forget."}
        target = ranked[0]
        with self._lock:
            self._notes = [n for n in self._notes if n["id"] != target["id"]]
            self._save()
        return {"success": True, "message": f"Forgotten: \"{target['text'][:60]}\""}

    # ── read ─────────────────────────────────────────────────────────────

    def recall(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        if not self._notes:
            return {"success": True, "message": "I haven't been asked to remember anything yet."}
        ranked = self._rank(query, top_k)
        if not ranked:
            return {"success": True, "message": "Nothing relevant in my notes."}
        if len(ranked) == 1:
            return {"success": True, "message": ranked[0]["text"], "data": {"notes": ranked}}
        lines = "\n".join(f"  • {n['text']}" for n in ranked)
        return {"success": True, "message": f"Here's what I remember:\n{lines}", "data": {"notes": ranked}}

    def list_notes(self) -> Dict[str, Any]:
        if not self._notes:
            return {"success": True, "message": "No saved notes yet."}
        lines = "\n".join(f"  • {n['text']}" for n in self._notes[-15:])
        return {"success": True, "message": f"{len(self._notes)} note(s):\n{lines}"}

    # ── ranking ──────────────────────────────────────────────────────────

    def _rank(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        query = (query or "").strip()
        if not query:
            return self._notes[-top_k:][::-1]
        q_emb = self._try_embed(query)
        scored: List[tuple] = []
        if q_emb:
            for n in self._notes:
                if n.get("embed"):
                    scored.append((self._cosine(q_emb, n["embed"]), n))
        if scored:
            scored.sort(key=lambda s: -s[0])
            return [n for score, n in scored[:top_k] if score > 0.2]
        # keyword fallback — overlap of lowercased word sets
        qwords = set(query.lower().split())
        for n in self._notes:
            overlap = len(qwords & set(n["text"].lower().split()))
            if overlap:
                scored.append((overlap, n))
        scored.sort(key=lambda s: -s[0])
        return [n for _, n in scored[:top_k]]

    def _try_embed(self, text: str) -> Optional[List[float]]:
        if self._rag and getattr(self._rag, "_embed_ok", False):
            try:
                return self._rag._embed(text)
            except Exception:
                return None
        return None

    @staticmethod
    def _cosine(a: List[float], b: List[float]) -> float:
        import math
        if not a or not b or len(a) != len(b):
            return 0.0
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(y * y for y in b))
        return dot / (na * nb) if na and nb else 0.0
