"""
WindowTiler — snap and tile application windows using Windows API (ctypes).
No pywin32 dependency; uses only ctypes which ships with Python.
"""

import ctypes
import ctypes.wintypes
import logging
from typing import Optional

logger = logging.getLogger(__name__)

user32 = ctypes.windll.user32
MONITOR_DEFAULTTONEAREST = 0x00000002

# ShowWindow constants
SW_RESTORE = 9
SW_SHOWNORMAL = 1


def _get_work_area() -> tuple[int, int, int, int]:
    """Return (left, top, right, bottom) of the primary monitor work area."""
    rc = ctypes.wintypes.RECT()
    user32.SystemParametersInfoW(48, 0, ctypes.byref(rc), 0)  # SPI_GETWORKAREA
    return rc.left, rc.top, rc.right, rc.bottom


def _hwnd_by_title(fragment: str) -> Optional[int]:
    """Find the first window whose title contains fragment (case-insensitive)."""
    result: list[int] = []
    frag_lower = fragment.lower()

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
    def _cb(hwnd, _):
        length = user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buf, length + 1)
            if frag_lower in buf.value.lower() and user32.IsWindowVisible(hwnd):
                result.append(hwnd)
        return True

    user32.EnumWindows(_cb, 0)
    return result[0] if result else None


def _move_window(hwnd: int, x: int, y: int, w: int, h: int) -> bool:
    user32.ShowWindow(hwnd, SW_RESTORE)
    return bool(user32.MoveWindow(hwnd, x, y, w, h, True))


class WindowTiler:
    LAYOUTS = {
        "left": "left half",
        "right": "right half",
        "top": "top half",
        "bottom": "bottom half",
        "topleft": "top-left quarter",
        "topright": "top-right quarter",
        "bottomleft": "bottom-left quarter",
        "bottomright": "bottom-right quarter",
        "maximize": "maximized",
        "center": "centered (80%)",
    }

    def _calc(self, layout: str) -> Optional[tuple[int, int, int, int]]:
        l, t, r, b = _get_work_area()
        W, H = r - l, b - t
        hw, hh = W // 2, H // 2
        plans = {
            "left":        (l,      t,  hw,  H),
            "right":       (l + hw, t,  hw,  H),
            "top":         (l,      t,  W,   hh),
            "bottom":      (l,      t + hh, W, hh),
            "topleft":     (l,      t,  hw,  hh),
            "topright":    (l + hw, t,  hw,  hh),
            "bottomleft":  (l,      t + hh, hw, hh),
            "bottomright": (l + hw, t + hh, hw, hh),
            "maximize":    (l,      t,  W,   H),
            "center":      (l + W // 10, t + H // 10, W * 8 // 10, H * 8 // 10),
        }
        return plans.get(layout.lower())

    def snap_window(self, layout: str, window_title: str = "") -> dict:
        """Snap the foreground (or named) window to a layout position."""
        coords = self._calc(layout)
        if not coords:
            return {
                "success": False,
                "message": f"Unknown layout '{layout}'. Choose from: {', '.join(self.LAYOUTS)}",
            }

        if window_title:
            hwnd = _hwnd_by_title(window_title)
            if not hwnd:
                return {"success": False, "message": f"No visible window matching '{window_title}'."}
        else:
            hwnd = user32.GetForegroundWindow()
            if not hwnd:
                return {"success": False, "message": "No foreground window found."}

        x, y, w, h = coords
        ok = _move_window(hwnd, x, y, w, h)
        label = self.LAYOUTS.get(layout.lower(), layout)
        if ok:
            return {"success": True, "message": f"Window snapped to {label}.", "data": {"x": x, "y": y, "w": w, "h": h}}
        return {"success": False, "message": "Failed to move window (may be a system window)."}

    def tile_all(self, layout: str = "grid") -> dict:
        """Tile all visible non-minimized windows in a grid."""
        windows: list[int] = []

        @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
        def _cb(hwnd, _):
            if user32.IsWindowVisible(hwnd) and not user32.IsIconic(hwnd):
                length = user32.GetWindowTextLengthW(hwnd)
                if length > 0:
                    windows.append(hwnd)
            return True

        user32.EnumWindows(_cb, 0)

        n = len(windows)
        if n == 0:
            return {"success": True, "message": "No visible windows to tile.", "data": {}}

        l, t, r, b = _get_work_area()
        W, H = r - l, b - t

        import math
        cols = math.ceil(math.sqrt(n))
        rows = math.ceil(n / cols)
        cw, ch = W // cols, H // rows

        for i, hwnd in enumerate(windows):
            row, col = divmod(i, cols)
            _move_window(hwnd, l + col * cw, t + row * ch, cw, ch)

        return {
            "success": True,
            "message": f"Tiled {n} windows in a {cols}×{rows} grid.",
            "data": {"count": n, "cols": cols, "rows": rows},
        }

    def list_layouts(self) -> dict:
        layouts = [{"id": k, "description": v} for k, v in self.LAYOUTS.items()]
        return {"success": True, "message": "Available window layouts.", "data": {"layouts": layouts}}
