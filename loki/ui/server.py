"""
FastAPI + WebSocket server — replaces PyQt6 UI.
The Next.js frontend connects via ws://localhost:7777/ws.

New endpoints (KORTEX-inspired):
  POST /upload           — index a file for RAG
  DELETE /upload/{name}  — remove file from index
  GET  /files            — list indexed files
  GET  /brain            — current brain memory state
  POST /brain/personality — switch personality mode
  GET  /audit            — recent audit log entries
"""

import asyncio
import json
import logging
import os
import shutil
import webbrowser
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

UI_DIST = Path(__file__).parent.parent.parent / "loki-ui" / "out"


class ConnectionManager:
    def __init__(self):
        self._connections: Set[WebSocket] = set()

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        self._connections.add(ws)
        logger.info(f"WebSocket connected — total: {len(self._connections)}")

    def disconnect(self, ws: WebSocket) -> None:
        self._connections.discard(ws)
        logger.info(f"WebSocket disconnected — total: {len(self._connections)}")

    async def broadcast(self, message: Dict[str, Any]) -> None:
        dead: List[WebSocket] = []
        for ws in list(self._connections):
            try:
                await ws.send_text(json.dumps(message))
            except Exception:
                dead.append(ws)
        for ws in dead:
            self._connections.discard(ws)

    @property
    def has_clients(self) -> bool:
        return len(self._connections) > 0


class LokiServer:
    """
    FastAPI server bridging Python backend ↔ Next.js UI.

    Callbacks wired by main.py:
      on_user_message(text: str)
      on_mute_toggle(muted: bool)
      on_undo()
    """

    def __init__(self, config: dict):
        self._cfg = config.get("ui", {})
        self._port = self._cfg.get("port", 7777)
        self._app = FastAPI(title="Loki AI")
        self._manager = ConnectionManager()
        self._loop: Optional[asyncio.AbstractEventLoop] = None

        # Component references (set by main.py after init)
        self._rag_engine = None
        self._brain_memory = None
        self._audit_log = None
        self._uploads_dir: Optional[Path] = None

        # Callbacks
        self.on_user_message: Optional[Callable[[str], None]] = None
        self.on_mute_toggle: Optional[Callable[[bool], None]] = None
        self.on_undo: Optional[Callable] = None

        self._setup_routes()

    def set_components(self, rag_engine=None, brain_memory=None, audit_log=None, uploads_dir=None):
        self._rag_engine = rag_engine
        self._brain_memory = brain_memory
        self._audit_log = audit_log
        self._uploads_dir = Path(uploads_dir) if uploads_dir else None

    # ─── Routes ───────────────────────────────────────────────────────────────

    def _setup_routes(self) -> None:
        app = self._app

        @app.websocket("/ws")
        async def websocket_endpoint(ws: WebSocket):
            await self._manager.connect(ws)
            try:
                while True:
                    raw = await ws.receive_text()
                    try:
                        msg = json.loads(raw)
                    except json.JSONDecodeError:
                        continue
                    await self._handle_client_message(msg)
            except WebSocketDisconnect:
                self._manager.disconnect(ws)

        @app.post("/upload")
        async def upload_file(file: UploadFile = File(...)):
            if not self._rag_engine:
                raise HTTPException(503, "RAG engine not initialized")
            if not self._rag_engine.is_available:
                raise HTTPException(503, "nomic-embed-text not available — run: ollama pull nomic-embed-text")

            uploads_dir = self._uploads_dir or Path("loki/memory/uploads")
            uploads_dir.mkdir(parents=True, exist_ok=True)
            dest = uploads_dir / file.filename

            content = await file.read()
            dest.write_bytes(content)

            result = self._rag_engine.index_file(dest)
            if result.get("success"):
                self._broadcast_sync({"type": "file_indexed", "filename": file.filename,
                                      "chunk_count": result.get("chunk_count", 0)})
            return JSONResponse(result)

        @app.delete("/upload/{filename}")
        async def delete_file(filename: str):
            if not self._rag_engine:
                raise HTTPException(503, "RAG engine not initialized")
            removed = self._rag_engine.delete_file(filename)
            uploads_dir = self._uploads_dir or Path("loki/memory/uploads")
            file_path = uploads_dir / filename
            if file_path.exists():
                file_path.unlink()
            return {"success": True, "chunks_removed": removed, "filename": filename}

        @app.get("/files")
        async def list_files():
            if not self._rag_engine:
                return {"files": [], "chunk_count": 0, "available": False}
            return {
                "files": self._rag_engine.indexed_files,
                "chunk_count": self._rag_engine.chunk_count,
                "available": self._rag_engine.is_available,
            }

        @app.get("/brain")
        async def get_brain():
            if not self._brain_memory:
                return {"error": "Brain memory not initialized"}
            return self._brain_memory.to_dict()

        @app.post("/brain/personality")
        async def set_personality(body: dict):
            mode = body.get("mode", "loki")
            if not self._brain_memory:
                raise HTTPException(503, "Brain memory not initialized")
            if mode not in ("loki", "jarvis", "friday"):
                raise HTTPException(400, f"Unknown personality: {mode}")
            self._brain_memory.personality = mode
            self._broadcast_sync({"type": "personality_changed", "mode": mode})
            return {"success": True, "personality": mode}

        @app.get("/audit")
        async def get_audit(n: int = 20):
            if not self._audit_log:
                return {"entries": []}
            return {"entries": self._audit_log.get_recent(n)}

        @app.get("/health")
        async def health():
            return {
                "status": "ok",
                "rag_available": bool(self._rag_engine and self._rag_engine.is_available),
                "brain_loaded": self._brain_memory is not None,
            }

        # Serve Next.js static export if built
        if UI_DIST.exists():
            app.mount("/", StaticFiles(directory=str(UI_DIST), html=True), name="ui")
        else:
            @app.get("/")
            async def root():
                return {"status": "Loki backend running", "note": "Run 'npm run build' in loki-ui/"}

    async def _handle_client_message(self, msg: dict) -> None:
        kind = msg.get("type")
        if kind == "user_message":
            text = msg.get("text", "").strip()
            if text and self.on_user_message:
                self.on_user_message(text)
        elif kind == "mute_toggle":
            muted = bool(msg.get("muted", False))
            if self.on_mute_toggle:
                self.on_mute_toggle(muted)
        elif kind == "undo":
            if self.on_undo:
                self.on_undo()

    # ─── Outbound helpers ─────────────────────────────────────────────────────

    def _broadcast_sync(self, payload: dict) -> None:
        if self._loop and self._loop.is_running():
            asyncio.run_coroutine_threadsafe(
                self._manager.broadcast(payload), self._loop
            )

    def add_system_message(self, text: str) -> None:
        self._broadcast_sync({"type": "system_message", "text": text})

    def add_user_message(self, text: str) -> None:
        self._broadcast_sync({"type": "user_message", "text": text})

    def add_loki_message(self, text: str) -> None:
        self._broadcast_sync({"type": "loki_message", "text": text})

    def set_status(self, status: str) -> None:
        self._broadcast_sync({"type": "status", "status": status})

    def update_transcript(self, text: str) -> None:
        self._broadcast_sync({"type": "transcript", "text": text})

    def clear_transcript(self) -> None:
        self._broadcast_sync({"type": "clear_transcript"})

    def show_window(self) -> None:
        self._broadcast_sync({"type": "show"})

    def hide_window(self) -> None:
        self._broadcast_sync({"type": "hide"})

    # ─── Lifecycle ────────────────────────────────────────────────────────────

    def get_app(self) -> FastAPI:
        return self._app

    def set_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        self._loop = loop

    def open_browser(self) -> None:
        webbrowser.open(f"http://localhost:{self._port}")


def create_loki_server(config: dict) -> LokiServer:
    return LokiServer(config)
