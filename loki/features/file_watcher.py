"""
FileWatcher — monitor directories for changes and trigger automated actions:
  - Backup trigger: backup a file when it changes (milestone files)
  - Media auto-convert: convert any media file dropped into a watched inbox folder
  - General change notifications

Uses threading + polling (no external watchdog dependency).
"""

import logging
import os
import threading
import time
from pathlib import Path
from typing import Callable, Optional

logger = logging.getLogger(__name__)

MEDIA_EXTENSIONS = {".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm",
                    ".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"}


class WatchJob:
    """A single directory watch job with a callback and state tracking."""

    def __init__(self, path: Path, callback: Callable[[Path, str], None],
                 poll_seconds: float = 5.0, recursive: bool = False,
                 extensions: Optional[set] = None):
        self.path = path
        self.callback = callback
        self.poll_seconds = poll_seconds
        self.recursive = recursive
        self.extensions = extensions
        self._snapshot: dict[str, float] = {}
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def _scan(self) -> dict[str, float]:
        result = {}
        try:
            glob = self.path.rglob("*") if self.recursive else self.path.iterdir()
            for fp in glob:
                if fp.is_file():
                    if self.extensions and fp.suffix.lower() not in self.extensions:
                        continue
                    try:
                        result[str(fp)] = fp.stat().st_mtime
                    except OSError:
                        pass
        except Exception:
            pass
        return result

    def _loop(self):
        self._snapshot = self._scan()
        while self._running:
            time.sleep(self.poll_seconds)
            current = self._scan()

            # New or modified files
            for fp_str, mtime in current.items():
                old_mtime = self._snapshot.get(fp_str)
                if old_mtime is None:
                    self.callback(Path(fp_str), "created")
                elif mtime != old_mtime:
                    self.callback(Path(fp_str), "modified")

            # Deleted files
            for fp_str in self._snapshot:
                if fp_str not in current:
                    self.callback(Path(fp_str), "deleted")

            self._snapshot = current

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True,
                                        name=f"watcher-{self.path.name}")
        self._thread.start()

    def stop(self):
        self._running = False


class FileWatcher:
    def __init__(self, backup_manager=None, media_converter=None):
        self._backup = backup_manager
        self._media = media_converter
        self._jobs: dict[str, WatchJob] = {}

    def _job_key(self, path: Path, job_type: str) -> str:
        return f"{job_type}:{path}"

    def watch_for_backup(self, file_or_dir: str, destination: Optional[str] = None,
                         poll_seconds: float = 30.0) -> dict:
        """Auto-backup a file or directory whenever it changes."""
        fp = Path(file_or_dir).expanduser().resolve()
        if not fp.exists():
            return {"success": False, "message": f"Path not found: {fp}"}

        if not self._backup:
            return {"success": False, "message": "BackupManager not available."}

        def _on_change(changed: Path, event: str):
            if event == "deleted":
                return
            logger.info("Auto-backup triggered: %s (%s)", changed, event)
            if fp.is_file():
                self._backup.backup_file(str(changed), destination)
            else:
                self._backup.backup_directory(str(changed), destination)

        watch_path = fp.parent if fp.is_file() else fp
        ext_filter = {fp.suffix.lower()} if fp.is_file() else None
        key = self._job_key(fp, "backup")

        if key in self._jobs:
            return {"success": True, "message": f"Already watching {fp.name} for backups."}

        job = WatchJob(watch_path, _on_change, poll_seconds=poll_seconds,
                       extensions=ext_filter)
        job.start()
        self._jobs[key] = job
        return {
            "success": True,
            "message": f"Auto-backup enabled for '{fp.name}' (checked every {int(poll_seconds)}s).",
            "data": {"path": str(fp), "destination": destination},
        }

    def watch_media_inbox(self, inbox_dir: str, output_format: str = "mp4",
                          poll_seconds: float = 10.0) -> dict:
        """Auto-convert any media file dropped into inbox_dir."""
        inbox = Path(inbox_dir).expanduser().resolve()
        inbox.mkdir(parents=True, exist_ok=True)

        if not self._media:
            return {"success": False, "message": "MediaConverter not available."}

        converting: set = set()

        def _on_change(fp: Path, event: str):
            if event != "created" or fp.suffix.lower() not in MEDIA_EXTENSIONS:
                return
            if str(fp) in converting:
                return
            if fp.suffix.lower() == f".{output_format}":
                return
            converting.add(str(fp))
            logger.info("Auto-converting: %s → %s", fp.name, output_format)
            try:
                self._media.convert(str(fp), output_format)
            except Exception as e:
                logger.error("Auto-convert failed: %s", e)
            converting.discard(str(fp))

        key = self._job_key(inbox, "media")
        if key in self._jobs:
            return {"success": True, "message": f"Already watching '{inbox.name}' for media."}

        job = WatchJob(inbox, _on_change, poll_seconds=poll_seconds,
                       extensions=MEDIA_EXTENSIONS)
        job.start()
        self._jobs[key] = job
        return {
            "success": True,
            "message": f"Media inbox active: drop files into '{inbox}' → auto-converted to {output_format}.",
            "data": {"inbox": str(inbox), "output_format": output_format},
        }

    def watch_custom(self, directory: str, poll_seconds: float = 5.0,
                     recursive: bool = False, extensions: Optional[str] = None) -> dict:
        """Start a custom watch job that logs all changes."""
        dp = Path(directory).expanduser().resolve()
        if not dp.exists():
            return {"success": False, "message": f"Directory not found: {dp}"}

        ext_set = None
        if extensions:
            ext_set = {e.strip().lower() if e.startswith(".") else f".{e.strip().lower()}"
                       for e in extensions.split(",")}

        changes: list[str] = []

        def _on_change(fp: Path, event: str):
            entry = f"[{event.upper()}] {fp}"
            changes.append(entry)
            logger.info("FileWatcher: %s", entry)

        key = self._job_key(dp, "custom")
        if key in self._jobs:
            return {"success": True, "message": f"Already watching '{dp.name}'."}

        job = WatchJob(dp, _on_change, poll_seconds=poll_seconds,
                       recursive=recursive, extensions=ext_set)
        job.start()
        self._jobs[key] = job
        return {
            "success": True,
            "message": f"Watching '{dp}' for changes (poll: {poll_seconds}s).",
            "data": {"directory": str(dp)},
        }

    def stop_watch(self, path: str) -> dict:
        """Stop all watch jobs for a given path."""
        stopped = []
        for key, job in list(self._jobs.items()):
            if str(Path(path).expanduser().resolve()) in key:
                job.stop()
                del self._jobs[key]
                stopped.append(key)
        if stopped:
            return {"success": True, "message": f"Stopped {len(stopped)} watcher(s).", "data": {"stopped": stopped}}
        return {"success": False, "message": f"No active watchers for '{path}'."}

    def list_watchers(self) -> dict:
        """List all active watch jobs."""
        if not self._jobs:
            return {"success": True, "message": "No active file watchers.", "data": {"watchers": []}}
        watchers = [{"key": k, "path": str(v.path), "running": v._running} for k, v in self._jobs.items()]
        msg = f"{len(watchers)} active watcher(s):\n" + "\n".join(f"  • {w['key']}" for w in watchers)
        return {"success": True, "message": msg, "data": {"watchers": watchers}}

    def stop_all(self) -> dict:
        """Stop all active watchers."""
        count = len(self._jobs)
        for job in self._jobs.values():
            job.stop()
        self._jobs.clear()
        return {"success": True, "message": f"Stopped {count} watcher(s).", "data": {}}
