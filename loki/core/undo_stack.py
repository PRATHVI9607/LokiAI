"""
Undo stack — reversible action history with 25-action depth.
"""

import os
import shutil
import logging
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class UndoEntry:
    action_type: str
    snapshot: Dict[str, Any]
    description: str
    undo_fn: Optional[Callable] = field(default=None, repr=False)


class UndoStack:
    """LIFO undo stack with per-type rollback logic."""

    MAX_DEPTH = 25

    def __init__(self, max_depth: int = MAX_DEPTH):
        self._stack: List[UndoEntry] = []
        self._max_depth = max_depth

    def push(self, action_type: str, snapshot: Dict[str, Any], description: str,
             undo_fn: Optional[Callable] = None) -> None:
        entry = UndoEntry(action_type=action_type, snapshot=snapshot,
                          description=description, undo_fn=undo_fn)
        self._stack.append(entry)
        if len(self._stack) > self._max_depth:
            self._stack.pop(0)
        logger.debug(f"Pushed undo: {description}")

    def pop_and_undo(self) -> bool:
        if not self._stack:
            return False
        entry = self._stack.pop()
        logger.info(f"Undoing: {entry.description}")

        if entry.undo_fn:
            try:
                entry.undo_fn(entry.snapshot)
                return True
            except Exception as e:
                logger.error(f"Custom undo failed: {e}")
                return False

        return self._builtin_undo(entry)

    def _builtin_undo(self, entry: UndoEntry) -> bool:
        snap = entry.snapshot
        try:
            if entry.action_type == "file_create":
                path = Path(snap["path"])
                if path.exists():
                    path.unlink()
                return True

            elif entry.action_type == "file_delete":
                path = Path(snap["path"])
                path.parent.mkdir(parents=True, exist_ok=True)
                with open(path, "wb") as f:
                    f.write(snap["content"])
                return True

            elif entry.action_type == "file_move":
                src, dst = Path(snap["src"]), Path(snap["dst"])
                if dst.exists():
                    shutil.move(str(dst), str(src))
                return True

            elif entry.action_type == "folder_create":
                path = Path(snap["path"])
                if path.exists():
                    shutil.rmtree(path)
                return True

            elif entry.action_type == "folder_delete":
                self._restore_tree(Path(snap["path"]), snap["tree"])
                return True

            elif entry.action_type == "volume_change":
                try:
                    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                    from comtypes import CLSCTX_ALL
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    vol = interface.QueryInterface(IAudioEndpointVolume)
                    vol.SetMasterVolumeLevelScalar(snap["previous"] / 100.0, None)
                    return True
                except Exception as e:
                    logger.error(f"Volume undo failed: {e}")
                    return False

            elif entry.action_type == "brightness_change":
                try:
                    import screen_brightness_control as sbc
                    sbc.set_brightness(snap["previous"])
                    return True
                except Exception as e:
                    logger.error(f"Brightness undo failed: {e}")
                    return False

        except Exception as e:
            logger.error(f"Undo failed ({entry.action_type}): {e}", exc_info=True)
            return False

        logger.warning(f"No undo handler for: {entry.action_type}")
        return False

    def _restore_tree(self, base: Path, tree: Dict) -> None:
        base.mkdir(parents=True, exist_ok=True)
        for name, content in tree.items():
            path = base / name
            if isinstance(content, dict):
                self._restore_tree(path, content)
            else:
                with open(path, "wb") as f:
                    f.write(content)

    def is_empty(self) -> bool:
        return len(self._stack) == 0

    def peek(self) -> Optional[UndoEntry]:
        return self._stack[-1] if self._stack else None

    def clear(self) -> None:
        self._stack.clear()

    def __len__(self) -> int:
        return len(self._stack)
