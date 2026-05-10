"""
FastAPI + WebSocket server — replaces PyQt6 UI.
The Next.js frontend connects via ws://localhost:7777/ws.
"""

import asyncio
import json
import logging
import os
import random
import webbrowser
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

logger = logging.getLogger(__name__)

UI_DIST = Path(__file__).parent.parent.parent / "loki-ui" / "out"


class ConnectionManager:
    """Manages active WebSocket connections."""

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
    FastAPI server that bridges the Python backend to the Next.js UI.

    Callbacks set by main.py:
      on_user_message(text: str)  — user typed/said something
      on_mute_toggle(muted: bool) — user toggled mic mute
      on_undo()                   — user pressed undo
    """

    def __init__(self, config: dict):
        self._cfg = config.get("ui", {})
        self._port = self._cfg.get("port", 7777)
        self._app = FastAPI(title="Loki AI")
        self._manager = ConnectionManager()
        self._loop: Optional[asyncio.AbstractEventLoop] = None

        self.on_user_message: Optional[Callable[[str], None]] = None
        self.on_mute_toggle: Optional[Callable[[bool], None]] = None
        self.on_undo: Optional[Callable] = None

        self._setup_routes()

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

    # ─── Outbound helpers (called from Python threads) ───────────────────────

    def _broadcast_sync(self, payload: dict) -> None:
        """Thread-safe broadcast: schedule on the event loop from any thread."""
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

    # ─── Lifecycle ───────────────────────────────────────────────────────────

    def get_app(self) -> FastAPI:
        return self._app

    def set_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        self._loop = loop

    def open_browser(self) -> None:
        webbrowser.open(f"http://localhost:{self._port}")


def create_loki_server(config: dict) -> LokiServer:
    return LokiServer(config)
