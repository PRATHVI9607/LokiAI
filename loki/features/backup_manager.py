"""
BackupManager — copy files/directories to a backup destination with timestamps.
"""

import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

DEFAULT_BACKUP_ROOT = Path.home() / "LokiBackups"


class BackupManager:
    def __init__(self, backup_root: Optional[str] = None):
        self._root = Path(backup_root).expanduser().resolve() if backup_root else DEFAULT_BACKUP_ROOT

    def backup_file(self, path: str, destination: Optional[str] = None) -> dict:
        """Copy a single file to the backup directory with a timestamp suffix."""
        src = Path(path).expanduser().resolve()
        if not src.exists() or not src.is_file():
            return {"success": False, "message": f"File not found: {path}"}

        dst_dir = Path(destination).expanduser().resolve() if destination else self._root / src.parent.name
        dst_dir.mkdir(parents=True, exist_ok=True)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        dst = dst_dir / f"{src.stem}_{ts}{src.suffix}"

        try:
            shutil.copy2(src, dst)
            size_kb = round(dst.stat().st_size / 1024, 1)
            return {
                "success": True,
                "message": f"Backed up {src.name} → {dst} ({size_kb} KB).",
                "data": {"source": str(src), "backup": str(dst)},
            }
        except Exception as e:
            return {"success": False, "message": f"Backup failed: {e}"}

    def backup_directory(self, path: str, destination: Optional[str] = None) -> dict:
        """Copy an entire directory tree to backup with a timestamp."""
        src = Path(path).expanduser().resolve()
        if not src.exists() or not src.is_dir():
            return {"success": False, "message": f"Directory not found: {path}"}

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        dst_base = Path(destination).expanduser().resolve() if destination else self._root
        dst = dst_base / f"{src.name}_{ts}"

        try:
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns(
                "__pycache__", "*.pyc", "node_modules", ".git", ".venv", ".next"
            ))
            # Count files
            n_files = sum(1 for _ in dst.rglob("*") if _.is_file())
            size_mb = round(sum(f.stat().st_size for f in dst.rglob("*") if f.is_file()) / 1048576, 2)
            return {
                "success": True,
                "message": f"Backed up {src.name}/ → {dst} ({n_files} files, {size_mb} MB).",
                "data": {"source": str(src), "backup": str(dst), "files": n_files, "size_mb": size_mb},
            }
        except Exception as e:
            return {"success": False, "message": f"Directory backup failed: {e}"}

    def list_backups(self, name_filter: Optional[str] = None) -> dict:
        """List existing backups."""
        if not self._root.exists():
            return {"success": True, "message": "No backups found.", "data": {"backups": []}}
        entries = []
        for item in sorted(self._root.rglob("*"), key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True):
            if name_filter and name_filter.lower() not in item.name.lower():
                continue
            try:
                entries.append({"path": str(item), "size_mb": round(item.stat().st_size / 1048576, 2) if item.is_file() else None})
            except Exception:
                pass
            if len(entries) >= 20:
                break
        msg = f"Found {len(entries)} backup entries." if entries else "No backups found."
        return {"success": True, "message": msg, "data": {"backups": entries, "root": str(self._root)}}
