"""
File organizer — auto-sort downloads and desktop by file type.
Restricted to Downloads and Desktop only to prevent repo/project damage.
"""

import shutil
import logging
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

DEFAULT_RULES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico", ".tiff"],
    "Documents": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md", ".odt"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"],
    "Code": [".py", ".js", ".ts", ".html", ".css", ".java", ".cpp", ".c", ".h", ".go", ".rs", ".rb", ".php"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
    "Executables": [".exe", ".msi", ".bat", ".cmd", ".ps1", ".sh"],
    "Data": [".json", ".xml", ".csv", ".yaml", ".yml", ".sql", ".db", ".sqlite"],
}

# Only these directories are safe to auto-organize
_SAFE_DIRS = frozenset([
    Path.home() / "Downloads",
    Path.home() / "Desktop",
])


class FileOrganizer:
    """Organize files in a directory by type."""

    def __init__(self, config: dict):
        self._rules = DEFAULT_RULES.copy()
        custom = config.get("rules", {})
        for category, exts in custom.items():
            if category in self._rules:
                self._rules[category].extend(exts)
            else:
                self._rules[category] = exts
        # Allow tests/config to extend the safe directory whitelist
        extra_safe = config.get("safe_dirs", [])
        self._safe_dirs = frozenset([
            *_SAFE_DIRS,
            *(Path(d).expanduser().resolve() for d in extra_safe),
        ])

    def _is_safe_dir(self, target: Path) -> bool:
        for safe in self._safe_dirs:
            try:
                if target == safe or target.is_relative_to(safe):
                    return True
            except Exception:
                if str(target).startswith(str(safe)):
                    return True
        return False

    def organize(self, directory: str = None) -> Dict[str, Any]:
        if directory:
            target = Path(directory).expanduser().resolve()
            if not self._is_safe_dir(target):
                return {
                    "success": False,
                    "message": (
                        f"Safety restriction: file organizer only works on Downloads and Desktop "
                        f"to prevent accidental damage to projects or system folders. "
                        f"Got: {target}"
                    ),
                }
        else:
            target = Path.home() / "Downloads"

        if not target.exists():
            return {"success": False, "message": f"Directory '{target}' not found."}

        # Build extension→category map
        ext_map: Dict[str, str] = {}
        for category, exts in self._rules.items():
            for ext in exts:
                ext_map[ext.lower()] = category

        moved = []
        errors = []

        for item in target.iterdir():
            if item.is_dir() or item.name.startswith("."):
                continue

            ext = item.suffix.lower()
            category = ext_map.get(ext, "Other")

            dest_dir = target / category
            dest_dir.mkdir(exist_ok=True)
            dest_file = dest_dir / item.name

            # Handle naming conflicts
            if dest_file.exists():
                stem = item.stem
                suffix = item.suffix
                counter = 1
                while dest_file.exists():
                    dest_file = dest_dir / f"{stem}_{counter}{suffix}"
                    counter += 1

            try:
                shutil.move(str(item), str(dest_file))
                moved.append(f"{item.name} → {category}/")
            except Exception as e:
                errors.append(f"Failed to move {item.name}: {e}")

        if not moved and not errors:
            return {"success": True, "message": f"'{target.name}' is already organized. Nothing to move."}

        lines = [f"Organized {len(moved)} file(s) in '{target.name}':"]
        for m in moved[:15]:
            lines.append(f"  • {m}")
        if len(moved) > 15:
            lines.append(f"  ... and {len(moved) - 15} more.")
        if errors:
            lines.append(f"\n{len(errors)} errors occurred.")

        return {"success": True, "message": "\n".join(lines), "data": {"moved": moved, "errors": errors}}
