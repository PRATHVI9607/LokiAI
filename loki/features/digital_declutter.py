"""
DigitalDeclutter — find duplicate files, large files, old/unused files, and suggest cleanup.
"""

import hashlib
import logging
import os
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", ".next", "dist", "build"}


class DigitalDeclutter:
    def _hash_file(self, path: Path, block_size: int = 65536) -> Optional[str]:
        try:
            h = hashlib.md5()
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(block_size), b""):
                    h.update(chunk)
            return h.hexdigest()
        except Exception:
            return None

    def find_duplicates(self, directory: str = "~") -> dict:
        """Find duplicate files by MD5 hash."""
        base = Path(directory).expanduser().resolve()
        if not base.exists():
            return {"success": False, "message": f"Directory not found: {directory}"}

        hashes: dict[str, list[str]] = defaultdict(list)
        scanned = 0
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for fname in files:
                fp = Path(root) / fname
                if fp.stat().st_size == 0:
                    continue
                h = self._hash_file(fp)
                if h:
                    hashes[h].append(str(fp))
                scanned += 1

        duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}
        total_wasted = 0
        dup_groups = []
        for h, paths in duplicates.items():
            size = Path(paths[0]).stat().st_size
            wasted = size * (len(paths) - 1)
            total_wasted += wasted
            dup_groups.append({"files": paths, "size_each_kb": round(size / 1024, 1), "wasted_kb": round(wasted / 1024, 1)})

        wasted_mb = round(total_wasted / 1048576, 2)
        msg = (
            f"Found {len(dup_groups)} duplicate groups wasting {wasted_mb} MB "
            f"(scanned {scanned} files in {base})."
            if dup_groups else f"No duplicates found in {base} ({scanned} files scanned)."
        )
        return {"success": True, "message": msg, "data": {"duplicates": dup_groups, "wasted_mb": wasted_mb, "scanned": scanned}}

    def find_large_files(self, directory: str = "~", threshold_mb: float = 100) -> dict:
        """Find files larger than threshold_mb."""
        base = Path(directory).expanduser().resolve()
        if not base.exists():
            return {"success": False, "message": f"Directory not found: {directory}"}

        threshold = threshold_mb * 1048576
        large = []
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for fname in files:
                fp = Path(root) / fname
                try:
                    size = fp.stat().st_size
                    if size >= threshold:
                        large.append({"path": str(fp), "size_mb": round(size / 1048576, 2)})
                except Exception:
                    pass

        large.sort(key=lambda x: x["size_mb"], reverse=True)
        msg = (
            f"Found {len(large)} files over {threshold_mb} MB:\n"
            + "\n".join(f"  {f['size_mb']} MB — {f['path']}" for f in large[:10])
            if large else f"No files over {threshold_mb} MB found."
        )
        return {"success": True, "message": msg, "data": {"large_files": large[:50], "threshold_mb": threshold_mb}}

    def find_old_files(self, directory: str = "~/Downloads", days: int = 180) -> dict:
        """Find files not accessed in the past N days."""
        base = Path(directory).expanduser().resolve()
        if not base.exists():
            return {"success": False, "message": f"Directory not found: {directory}"}

        cutoff = datetime.now() - timedelta(days=days)
        old = []
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for fname in files:
                fp = Path(root) / fname
                try:
                    mtime = datetime.fromtimestamp(fp.stat().st_mtime)
                    if mtime < cutoff:
                        old.append({"path": str(fp), "last_modified": mtime.strftime("%Y-%m-%d"), "size_mb": round(fp.stat().st_size / 1048576, 2)})
                except Exception:
                    pass

        old.sort(key=lambda x: x["last_modified"])
        total_mb = round(sum(f["size_mb"] for f in old), 2)
        msg = (
            f"Found {len(old)} files not modified in {days}+ days ({total_mb} MB total):\n"
            + "\n".join(f"  {f['last_modified']} — {f['path']}" for f in old[:10])
            if old else f"No files older than {days} days in {base}."
        )
        return {"success": True, "message": msg, "data": {"old_files": old[:100], "total_mb": total_mb}}

    def suggest_cleanup(self, directory: str = "~") -> dict:
        """Run all checks and return a combined cleanup report."""
        dups = self.find_duplicates(directory)
        large = self.find_large_files(directory, threshold_mb=500)
        old = self.find_old_files(directory, days=180)

        parts = ["Declutter report:"]
        if dups["success"]:
            parts.append(f"• Duplicates: {dups['message']}")
        if large["success"]:
            parts.append(f"• Large files: {large['message'].split(chr(10))[0]}")
        if old["success"]:
            parts.append(f"• Old files: {old['message'].split(chr(10))[0]}")

        return {"success": True, "message": "\n".join(parts), "data": {"duplicates": dups.get("data"), "large": large.get("data"), "old": old.get("data")}}
