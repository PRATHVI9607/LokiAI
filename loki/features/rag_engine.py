"""
RAG engine — index uploaded files, query by semantic similarity.

Uses Ollama's nomic-embed-text for embeddings (fully local, no API key).
Stores a lightweight JSON vector index — no ChromaDB dependency.
"""

import json
import logging
import math
import re
import textwrap
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

import numpy as np
import requests

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java",
    ".cpp", ".c", ".h", ".cs", ".rb", ".php", ".swift",
    ".md", ".txt", ".yaml", ".yml", ".json", ".toml", ".ini",
    ".html", ".css", ".sh", ".bat", ".ps1", ".sql",
}

CHUNK_SIZE = 400    # words per chunk
CHUNK_OVERLAP = 40  # word overlap between chunks
SIMILARITY_THRESHOLD = 0.45


class RagEngine:
    """
    File RAG with Ollama nomic-embed-text embeddings.

    Index: list of chunks stored as JSON. Each chunk has:
      id, source (filename), chunk_idx, text, embedding (list of floats)

    Querying: cosine similarity between query embedding and all stored embeddings.
    """

    def __init__(self, memory_dir: Path, ollama_url: str = "http://localhost:11434"):
        self._dir = Path(memory_dir)
        self._dir.mkdir(parents=True, exist_ok=True)
        self._index_path = self._dir / "rag_index.json"
        self._uploads_dir = self._dir / "uploads"
        self._uploads_dir.mkdir(exist_ok=True)
        self._ollama_url = ollama_url.rstrip("/")

        self._chunks: List[Dict[str, Any]] = []
        self._available = False
        self._load_index()
        self._check_availability()

    def _check_availability(self) -> None:
        try:
            resp = requests.get(f"{self._ollama_url}/api/tags", timeout=3)
            if resp.status_code == 200:
                models = [m["name"] for m in resp.json().get("models", [])]
                if any("nomic-embed-text" in m for m in models):
                    self._available = True
                    logger.info("RAG engine: nomic-embed-text available")
                else:
                    logger.warning("RAG engine: nomic-embed-text not pulled. Run: ollama pull nomic-embed-text")
        except Exception:
            logger.warning("RAG engine: Ollama not reachable — file indexing disabled")

    def _load_index(self) -> None:
        if self._index_path.exists():
            try:
                with open(self._index_path, "r", encoding="utf-8") as f:
                    self._chunks = json.load(f)
                logger.info(f"RAG index loaded: {len(self._chunks)} chunks")
            except Exception as e:
                logger.error(f"RAG index load failed: {e}")
                self._chunks = []

    def _save_index(self) -> None:
        try:
            with open(self._index_path, "w", encoding="utf-8") as f:
                json.dump(self._chunks, f, ensure_ascii=False)
        except Exception as e:
            logger.error(f"RAG index save failed: {e}")

    # ─── Embedding ────────────────────────────────────────────────────────────

    def _embed(self, text: str) -> Optional[np.ndarray]:
        try:
            resp = requests.post(
                f"{self._ollama_url}/api/embed",
                json={"model": "nomic-embed-text", "input": text},
                timeout=30,
            )
            data = resp.json()
            emb = data.get("embeddings", [[]])[0]
            if emb:
                return np.array(emb, dtype=np.float32)
        except Exception as e:
            logger.error(f"Embedding error: {e}")
        return None

    # ─── Chunking ─────────────────────────────────────────────────────────────

    @staticmethod
    def _chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
        words = text.split()
        if not words:
            return []
        chunks = []
        i = 0
        while i < len(words):
            chunk_words = words[i:i + chunk_size]
            chunks.append(" ".join(chunk_words))
            i += chunk_size - overlap
        return chunks

    @staticmethod
    def _extract_text(path: Path) -> str:
        suffix = path.suffix.lower()
        try:
            if suffix == ".pdf":
                try:
                    import fitz  # PyMuPDF
                    doc = fitz.open(str(path))
                    return "\n".join(page.get_text() for page in doc)
                except ImportError:
                    logger.warning("PyMuPDF not installed — PDF text extraction unavailable")
                    return ""
            else:
                return path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            logger.error(f"Text extraction failed for {path}: {e}")
            return ""

    # ─── Public API ───────────────────────────────────────────────────────────

    @property
    def is_available(self) -> bool:
        return self._available

    @property
    def indexed_files(self) -> List[str]:
        seen = set()
        files = []
        for c in self._chunks:
            src = c.get("source", "")
            if src not in seen:
                seen.add(src)
                files.append(src)
        return files

    @property
    def chunk_count(self) -> int:
        return len(self._chunks)

    def index_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Index a file: extract text, chunk, embed, store.
        Returns {success, filename, chunk_count, message}.
        """
        if not self._available:
            return {
                "success": False,
                "message": "RAG unavailable — run: ollama pull nomic-embed-text",
            }

        path = Path(file_path)
        if not path.exists():
            return {"success": False, "message": f"File not found: {path}"}

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS and path.suffix.lower() != ".pdf":
            return {"success": False, "message": f"Unsupported file type: {path.suffix}"}

        # Remove existing chunks for this file
        filename = path.name
        self._chunks = [c for c in self._chunks if c.get("source") != filename]

        text = self._extract_text(path)
        if not text.strip():
            return {"success": False, "message": "File appears empty or unreadable."}

        chunks = self._chunk_text(text)
        new_chunks = []
        for i, chunk in enumerate(chunks):
            emb = self._embed(chunk)
            if emb is None:
                continue
            new_chunks.append({
                "source": filename,
                "chunk_idx": i,
                "text": chunk,
                "embedding": emb.tolist(),
                "indexed_at": datetime.now().isoformat(),
            })

        self._chunks.extend(new_chunks)
        self._save_index()

        logger.info(f"Indexed {filename}: {len(new_chunks)} chunks")
        return {
            "success": True,
            "filename": filename,
            "chunk_count": len(new_chunks),
            "message": f"Indexed {filename} — {len(new_chunks)} chunks ready.",
        }

    def query(self, text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Return top-K most semantically similar chunks.
        Each result: {text, source, chunk_idx, score}.
        """
        if not self._available or not self._chunks:
            return []

        query_emb = self._embed(text)
        if query_emb is None:
            return []

        embeddings = np.array([c["embedding"] for c in self._chunks], dtype=np.float32)
        q_norm = np.linalg.norm(query_emb)
        e_norms = np.linalg.norm(embeddings, axis=1)
        scores = (embeddings @ query_emb) / (e_norms * q_norm + 1e-10)

        top_indices = np.argsort(scores)[::-1][:top_k]
        results = []
        for idx in top_indices:
            score = float(scores[idx])
            if score < SIMILARITY_THRESHOLD:
                continue
            c = self._chunks[int(idx)]
            results.append({
                "text": c["text"],
                "source": c["source"],
                "chunk_idx": c["chunk_idx"],
                "score": round(score, 3),
            })
        return results

    def format_context(self, results: List[Dict[str, Any]]) -> str:
        """Format query results into a context block for the LLM."""
        if not results:
            return ""
        lines = ["## Context from your files:"]
        for r in results:
            lines.append(f"\n### {r['source']} (chunk {r['chunk_idx']}, relevance {r['score']})")
            lines.append(r["text"])
        return "\n".join(lines)

    def delete_file(self, filename: str) -> int:
        """Remove all chunks for a file. Returns number of chunks removed."""
        before = len(self._chunks)
        self._chunks = [c for c in self._chunks if c.get("source") != filename]
        removed = before - len(self._chunks)
        if removed:
            self._save_index()
        return removed

    def clear_index(self) -> None:
        self._chunks = []
        self._save_index()
