"""
File operations — create, delete, move with security constraints and undo.
Paths must be within one of the configured trusted roots (home + extra_roots).
"""

import os
import shutil
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

from loki.core.paths import resolve_within_roots

logger = logging.getLogger(__name__)

# Undo safety limits — deleting a file/folder snapshots its bytes into the in-memory
# undo stack. Without caps, deleting a few large files could exhaust RAM, and a deeply
# nested / symlink-looped tree could blow the Python recursion limit.
MAX_UNDO_FILE_BYTES = 50_000_000   # 50 MB — files above this delete WITHOUT undo
MAX_UNDO_TREE_DEPTH = 25           # folder snapshot recursion cap


class FileOps:
    """Secure file/folder operations with undo support."""

    def __init__(self, undo_stack, extra_roots: Optional[List[Path]] = None):
        self._undo = undo_stack
        self._home = Path(os.path.expanduser("~")).resolve()
        self._trusted_roots: List[Path] = [self._home]
        if extra_roots:
            self._trusted_roots.extend(Path(r).resolve() for r in extra_roots)

    def _safe(self, path: str) -> tuple[bool, Path]:
        """Returns (is_safe, resolved_path). Prevents path traversal outside trusted roots.
        Delegates to the shared `resolve_within_roots` helper (single source of truth)."""
        return resolve_within_roots(path, self._trusted_roots)

    def _deny(self, reason: str = "Access denied. Path is outside allowed directories.") -> Dict:
        return {"success": False, "message": reason}

    def create_file(self, path: str, content: str = "") -> Dict[str, Any]:
        safe, resolved = self._safe(path)
        if not safe:
            logger.warning(f"Blocked file_create: {path}")
            return self._deny()
        if resolved.exists():
            return {"success": False, "message": f"'{resolved.name}' already exists."}
        try:
            resolved.parent.mkdir(parents=True, exist_ok=True)
            self._undo.push("file_create", {"path": str(resolved)}, f"Created {resolved.name}")
            resolved.write_text(content, encoding="utf-8")
            logger.info(f"Created file: {resolved}")
            return {"success": True, "message": f"Done. '{resolved.name}' created."}
        except PermissionError:
            return self._deny("Permission denied creating that file.")
        except Exception as e:
            logger.error(f"file_create error: {e}")
            return {"success": False, "message": "File creation failed."}

    def create_folder(self, path: str) -> Dict[str, Any]:
        safe, resolved = self._safe(path)
        if not safe:
            return self._deny()
        if resolved.exists():
            return {"success": False, "message": f"'{resolved.name}' already exists."}
        try:
            self._undo.push("folder_create", {"path": str(resolved)}, f"Created folder {resolved.name}")
            resolved.mkdir(parents=True, exist_ok=True)
            return {"success": True, "message": f"Done. Folder '{resolved.name}' created."}
        except Exception as e:
            logger.error(f"folder_create error: {e}")
            return {"success": False, "message": "Folder creation failed."}

    def delete_file(self, path: str) -> Dict[str, Any]:
        safe, resolved = self._safe(path)
        if not safe:
            return self._deny()
        if not resolved.is_file():
            return {"success": False, "message": f"'{resolved.name}' is not a file or doesn't exist."}
        try:
            # Only snapshot for undo when the file is small enough to hold in RAM.
            # Large files are still deleted — but without undo (we say so plainly).
            size = resolved.stat().st_size
            undo_note = ""
            if size <= MAX_UNDO_FILE_BYTES:
                content = resolved.read_bytes()
                self._undo.push("file_delete", {"path": str(resolved), "content": content},
                                f"Deleted {resolved.name}")
            else:
                undo_note = f" (too large at {size / 1_000_000:.0f}MB to undo)"
            resolved.unlink()
            return {"success": True, "message": f"Done. '{resolved.name}' deleted{undo_note}."}
        except PermissionError:
            return self._deny("Permission denied deleting that file.")
        except Exception as e:
            logger.error(f"file_delete error: {e}")
            return {"success": False, "message": "File deletion failed."}

    def delete_folder(self, path: str) -> Dict[str, Any]:
        safe, resolved = self._safe(path)
        if not safe:
            return self._deny()
        if not resolved.is_dir():
            return {"success": False, "message": f"'{resolved.name}' is not a directory or doesn't exist."}
        try:
            tree = self._build_tree(resolved)
            self._undo.push("folder_delete", {"path": str(resolved), "tree": tree},
                            f"Deleted folder {resolved.name}")
            shutil.rmtree(resolved)
            return {"success": True, "message": f"Done. Folder '{resolved.name}' deleted."}
        except PermissionError:
            return self._deny("Permission denied deleting that folder.")
        except Exception as e:
            logger.error(f"folder_delete error: {e}")
            return {"success": False, "message": "Folder deletion failed."}

    def move(self, src: str, dst: str) -> Dict[str, Any]:
        src_safe, src_path = self._safe(src)
        dst_safe, dst_path = self._safe(dst)
        if not src_safe or not dst_safe:
            return self._deny()
        if not src_path.exists():
            return {"success": False, "message": f"Source '{src_path.name}' doesn't exist."}
        if dst_path.exists():
            return {"success": False, "message": f"Destination '{dst_path.name}' already exists."}
        try:
            self._undo.push("file_move", {"src": str(src_path), "dst": str(dst_path)},
                            f"Moved {src_path.name}")
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src_path), str(dst_path))
            return {"success": True, "message": f"Done. Moved '{src_path.name}' → '{dst_path.parent.name}'."}
        except Exception as e:
            logger.error(f"move error: {e}")
            return {"success": False, "message": "Move operation failed."}

    def _build_tree(self, path: Path, depth: int = 0) -> Dict:
        # Depth cap guards against symlink loops / pathological nesting blowing the
        # recursion limit; size cap keeps the in-memory undo snapshot bounded.
        if depth > MAX_UNDO_TREE_DEPTH:
            logger.warning(f"Folder nesting exceeds {MAX_UNDO_TREE_DEPTH} levels — undo truncated below {path}")
            return {}
        tree = {}
        try:
            for item in path.iterdir():
                if item.is_symlink():
                    continue  # never follow symlinks when snapshotting
                if item.is_file():
                    try:
                        if item.stat().st_size <= MAX_UNDO_FILE_BYTES:
                            tree[item.name] = item.read_bytes()
                        else:
                            tree[item.name] = b""  # too large to snapshot; restored empty
                    except Exception:
                        tree[item.name] = b""
                elif item.is_dir():
                    tree[item.name] = self._build_tree(item, depth + 1)
        except (OSError, PermissionError) as e:
            logger.warning(f"_build_tree error at {path}: {e}")
        return tree
