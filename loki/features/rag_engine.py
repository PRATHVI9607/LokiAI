"""
RAG engine — ChromaDB vector store with nomic-embed-text embeddings.

Replaces the flat JSON/numpy store with ChromaDB for:
- HNSW indexed queries (sub-ms regardless of corpus size)
- Persistent collection — no re-index on restart
- Metadata filtering by source, date, type
- Cosine similarity via ChromaDB's built-in distance metric
"""

import hashlib
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java",
    ".cpp", ".c", ".h", ".cs", ".rb", ".php", ".swift",
    ".md", ".txt", ".yaml", ".yml", ".json", ".toml", ".ini",
    ".html", ".css", ".sh", ".bat", ".ps1", ".sql",
}

CHUNK_SIZE = 400
CHUNK_OVERLAP = 40
TOP_K = 8
# ChromaDB cosine distance: 0=identical, 2=opposite → similarity = 1 - dist/2
# 0.5 similarity = 0.5 cosine sim — good balance of precision vs recall
SIMILARITY_THRESHOLD = 0.50


class RagEngine:
    """
    File RAG with ChromaDB (HNSW) + Ollama nomic-embed-text embeddings.
    One persistent collection: loki_rag.
    """

    def __init__(self, memory_dir: Path, ollama_url: str = "http://localhost:11434"):
        self._dir = Path(memory_dir)
        self._dir.mkdir(parents=True, exist_ok=True)
        self._ollama_url = ollama_url.rstrip("/")

        self._chroma_ok = False
        self._embed_ok = False
        self._client = None
        self._collection = None

        self._init_chroma()
        self._check_embed()

    # ─── Init ─────────────────────────────────────────────────────────────────

    def _init_chroma(self) -> None:
        try:
            import chromadb
            chroma_path = self._dir / "chroma"
            chroma_path.mkdir(exist_ok=True)
            self._client = chromadb.PersistentClient(path=str(chroma_path))
            self._collection = self._client.get_or_create_collection(
                name="loki_rag",
                metadata={"hnsw:space": "cosine"},
            )
            self._chroma_ok = True
            logger.info(f"ChromaDB ready — {self._collection.count()} chunks stored")
        except ImportError:
            logger.warning("chromadb not installed — run: pip install chromadb")
        except Exception as e:
            logger.error(f"ChromaDB init failed: {e}")

    def _check_embed(self) -> None:
        try:
            resp = requests.get(f"{self._ollama_url}/api/tags", timeout=3)
            if resp.status_code == 200:
                models = [m["name"] for m in resp.json().get("models", [])]
                if any("nomic-embed-text" in m for m in models):
                    self._embed_ok = True
                    logger.info("RAG embeddings: nomic-embed-text available")
                else:
                    logger.warning("RAG: nomic-embed-text not pulled. Run: ollama pull nomic-embed-text")
        except Exception:
            logger.warning("RAG: Ollama not reachable — embeddings disabled")

    # ─── Embedding ────────────────────────────────────────────────────────────

    def _embed(self, text: str) -> Optional[List[float]]:
        try:
            resp = requests.post(
                f"{self._ollama_url}/api/embed",
                json={"model": "nomic-embed-text", "input": text},
                timeout=30,
            )
            resp.raise_for_status()
            emb = resp.json().get("embeddings", [[]])[0]
            return emb if emb else None
        except Exception as e:
            logger.error(f"Embedding error: {e}")
            return None

    # ─── Chunking ─────────────────────────────────────────────────────────────

    @staticmethod
    def _chunk_text(text: str) -> List[str]:
        words = text.split()
        if not words:
            return []
        chunks = []
        i = 0
        while i < len(words):
            chunks.append(" ".join(words[i:i + CHUNK_SIZE]))
            i += CHUNK_SIZE - CHUNK_OVERLAP
        return chunks

    @staticmethod
    def _extract_text(path: Path) -> str:
        try:
            if path.suffix.lower() == ".pdf":
                try:
                    import fitz
                    with fitz.open(str(path)) as doc:
                        return "\n".join(p.get_text() for p in doc)
                except ImportError:
                    logger.warning("PyMuPDF not installed — PDF extraction unavailable")
                    return ""
            return path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            logger.error(f"Text extraction failed for {path}: {e}")
            return ""

    # ─── Properties ───────────────────────────────────────────────────────────

    @property
    def is_available(self) -> bool:
        return self._chroma_ok and self._embed_ok

    @property
    def indexed_files(self) -> List[str]:
        if not self._collection:
            return []
        try:
            result = self._collection.get(include=["metadatas"])
            seen: set = set()
            files = []
            for meta in result.get("metadatas", []):
                src = meta.get("source", "")
                if src and src not in seen:
                    seen.add(src)
                    files.append(src)
            return files
        except Exception:
            return []

    @property
    def chunk_count(self) -> int:
        if not self._collection:
            return 0
        try:
            return self._collection.count()
        except Exception:
            return 0

    # ─── Indexing ─────────────────────────────────────────────────────────────

    def index_file(self, file_path: Path) -> Dict[str, Any]:
        if not self.is_available:
            return {"success": False, "message": "RAG unavailable — check Ollama + chromadb install"}

        path = Path(file_path)
        if not path.exists():
            return {"success": False, "message": f"File not found: {path}"}
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS and path.suffix.lower() != ".pdf":
            return {"success": False, "message": f"Unsupported file type: {path.suffix}"}

        filename = path.name

        # Delete existing chunks for this file before re-indexing
        try:
            existing = self._collection.get(where={"source": filename})
            if existing["ids"]:
                self._collection.delete(ids=existing["ids"])
        except Exception:
            pass

        text = self._extract_text(path)
        if not text.strip():
            return {"success": False, "message": "File appears empty or unreadable."}

        chunks = self._chunk_text(text)
        ids, embeddings, documents, metadatas = [], [], [], []

        for i, chunk in enumerate(chunks):
            emb = self._embed(chunk)
            if emb is None:
                continue
            chunk_id = hashlib.md5(f"{filename}:{i}:{chunk[:50]}".encode()).hexdigest()
            ids.append(chunk_id)
            embeddings.append(emb)
            documents.append(chunk)
            metadatas.append({
                "source": filename,
                "chunk_idx": i,
                "indexed_at": datetime.now().isoformat(),
            })

        if ids:
            self._collection.upsert(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
            )

        logger.info(f"Indexed {filename}: {len(ids)} chunks → ChromaDB")
        return {
            "success": True,
            "filename": filename,
            "chunk_count": len(ids),
            "message": f"Indexed {filename} — {len(ids)} chunks ready.",
        }

    # ─── Querying ─────────────────────────────────────────────────────────────

    def query(self, text: str, top_k: int = TOP_K) -> List[Dict[str, Any]]:
        if not self.is_available or self.chunk_count == 0:
            return []

        query_emb = self._embed(text)
        if query_emb is None:
            return []

        try:
            results = self._collection.query(
                query_embeddings=[query_emb],
                n_results=min(top_k, self.chunk_count),
                include=["documents", "metadatas", "distances"],
            )
        except Exception as e:
            logger.error(f"ChromaDB query failed: {e}")
            return []

        output = []
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            # cosine distance [0,2] → similarity [0,1]
            similarity = 1.0 - (dist / 2.0)
            if similarity < SIMILARITY_THRESHOLD:
                continue
            output.append({
                "text": doc,
                "source": meta.get("source", "unknown"),
                "chunk_idx": meta.get("chunk_idx", 0),
                "score": round(similarity, 3),
            })

        return output

    def format_context(self, results: List[Dict[str, Any]]) -> str:
        if not results:
            return ""
        lines = ["## Context from your files:"]
        for r in results:
            lines.append(f"\n### {r['source']} (chunk {r['chunk_idx']}, relevance {r['score']})")
            lines.append(r["text"])
        return "\n".join(lines)

    # ─── Management ───────────────────────────────────────────────────────────

    def delete_file(self, filename: str) -> int:
        if not self._collection:
            return 0
        try:
            existing = self._collection.get(where={"source": filename})
            if existing["ids"]:
                self._collection.delete(ids=existing["ids"])
                return len(existing["ids"])
        except Exception as e:
            logger.error(f"Delete failed: {e}")
        return 0

    def clear_index(self) -> None:
        if not self._client:
            return
        try:
            self._client.delete_collection("loki_rag")
            self._collection = self._client.get_or_create_collection(
                name="loki_rag",
                metadata={"hnsw:space": "cosine"},
            )
            logger.info("RAG index cleared")
        except Exception as e:
            logger.error(f"Clear failed: {e}")
