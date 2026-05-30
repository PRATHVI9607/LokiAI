"""
SpotifyIntegration — control playback + see what's playing.

"What's playing?", "play", "pause", "skip", "next track", "previous".

ONE-TIME SETUP (optional — degrades gracefully without it):
  1. https://developer.spotify.com/dashboard → create an app
  2. Add redirect URI:  http://localhost:8888/callback
  3. Put the credentials in loki/.env:
        SPOTIFY_CLIENT_ID=...
        SPOTIFY_CLIENT_SECRET=...
  4. First use opens a browser to authorize (needs Spotify Premium for
     playback control; "what's playing" works on free too).

Requires `spotipy` (in requirements). Until configured, every method returns a
friendly setup message instead of crashing.
"""

import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

_SCOPES = "user-read-playback-state user-modify-playback-state user-read-currently-playing"
_REDIRECT = "http://localhost:8888/callback"

_SETUP_MSG = (
    "Spotify isn't connected. One-time setup: create an app at "
    "developer.spotify.com/dashboard, add redirect http://localhost:8888/callback, "
    "and put SPOTIFY_CLIENT_ID + SPOTIFY_CLIENT_SECRET in loki/.env. Then ask again."
)


class SpotifyIntegration:
    def __init__(self, memory_dir: Path):
        self._cache = Path(memory_dir).parent / "credentials" / "spotify_token.json"
        self._client_id = os.getenv("SPOTIFY_CLIENT_ID", "").strip()
        self._client_secret = os.getenv("SPOTIFY_CLIENT_SECRET", "").strip()
        self._sp = None
        self._available = bool(self._client_id and self._client_secret)
        if not self._available:
            logger.info("Spotify not configured (no client id/secret) — optional")

    def _ensure(self) -> bool:
        if self._sp:
            return True
        if not self._available:
            return False
        try:
            import spotipy
            from spotipy.oauth2 import SpotifyOAuth
            self._cache.parent.mkdir(parents=True, exist_ok=True)
            auth = SpotifyOAuth(
                client_id=self._client_id,
                client_secret=self._client_secret,
                redirect_uri=_REDIRECT,
                scope=_SCOPES,
                cache_path=str(self._cache),
                open_browser=True,
            )
            self._sp = spotipy.Spotify(auth_manager=auth)
            return True
        except Exception as e:
            logger.error(f"Spotify auth failed: {e}")
            return False

    # ── playback ─────────────────────────────────────────────────────────

    def now_playing(self) -> Dict[str, Any]:
        if not self._ensure():
            return {"success": False, "message": _SETUP_MSG}
        try:
            cur = self._sp.current_playback()
            if not cur or not cur.get("item"):
                return {"success": True, "message": "Nothing is playing right now."}
            item = cur["item"]
            artists = ", ".join(a["name"] for a in item.get("artists", []))
            state = "Playing" if cur.get("is_playing") else "Paused"
            return {"success": True,
                    "message": f"{state}: {item['name']} — {artists}",
                    "data": {"track": item["name"], "artists": artists}}
        except Exception as e:
            return {"success": False, "message": f"Spotify read failed: {e}"}

    def _control(self, action: str) -> Dict[str, Any]:
        if not self._ensure():
            return {"success": False, "message": _SETUP_MSG}
        try:
            if action == "play":
                self._sp.start_playback(); msg = "Playing."
            elif action == "pause":
                self._sp.pause_playback(); msg = "Paused."
            elif action == "next":
                self._sp.next_track(); msg = "Skipped."
            elif action == "previous":
                self._sp.previous_track(); msg = "Back a track."
            else:
                return {"success": False, "message": f"Unknown Spotify action: {action}"}
            return {"success": True, "message": msg}
        except Exception as e:
            # Most common cause: no active device / not Premium
            return {"success": False,
                    "message": f"Spotify control failed ({e}). Open Spotify on a device first; "
                               "playback control needs Premium."}

    def play(self) -> Dict[str, Any]:     return self._control("play")
    def pause(self) -> Dict[str, Any]:    return self._control("pause")
    def next(self) -> Dict[str, Any]:     return self._control("next")
    def previous(self) -> Dict[str, Any]: return self._control("previous")

    def search_play(self, query: str) -> Dict[str, Any]:
        if not self._ensure():
            return {"success": False, "message": _SETUP_MSG}
        try:
            res = self._sp.search(q=query, type="track", limit=1)
            items = res.get("tracks", {}).get("items", [])
            if not items:
                return {"success": True, "message": f"No track found for '{query}'."}
            track = items[0]
            self._sp.start_playback(uris=[track["uri"]])
            artists = ", ".join(a["name"] for a in track.get("artists", []))
            return {"success": True, "message": f"Playing {track['name']} — {artists}."}
        except Exception as e:
            return {"success": False,
                    "message": f"Couldn't play '{query}' ({e}). Open Spotify on a device first (Premium needed)."}

    @property
    def is_available(self) -> bool:
        return self._available
