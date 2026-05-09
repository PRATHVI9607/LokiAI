"""
File operations — create, delete, move with security constraints and undo.
All paths must be within user home directory.
"""

import os
import shutil
import logging
from typing import Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class FileOps:
    """Secure file/folder operations with undo support."""

    def __init__(self, undo_stack):
        self._undo = undo_stack
        self._home = Path(os.path.expanduser("~")).resolve()

    def _safe(self, path: str) -> tuple[bool, Path]:
        """Returns (is_safe, resolved_path). Prevents path traversal."""
        if not path or not path.strip():
            return False, Path()
        try:
            resolved = Path(path).expanduser().resolve()
            return resolved.is_relative_to(self._home), resolved
        except Exception:
            return False, Path()

    def _deny(self, reason: str = "Access denied. Stay within your home directory.") -> Dict:
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
            content = resolved.read_bytes()
            self._undo.push("file_delete", {"path": str(resolved), "content": content},
                            f"Deleted {resolved.name}")
            resolved.unlink()
            return {"success": True, "message": f"Done. '{resolved.name}' deleted."}
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

    def _build_tree(self, path: Path) -> Dict:
        tree = {}
        for item in path.iterdir():
            if item.is_file():
                try:
                    tree[item.name] = item.read_bytes()
                except Exception:
                    tree[item.name] = b""
            elif item.is_dir():
                tree[item.name] = self._build_tree(item)
        return tree
