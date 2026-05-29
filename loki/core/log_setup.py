"""
Loki logging — clean, color-coded terminal output with organized component tags.

Terminal shows a readable, aligned, color-coded view of what Loki is doing.
The file log (loki.log) keeps the full detailed format for debugging.

Noisy third-party loggers (httpx, comtypes, urllib3, openai, etc.) are
suppressed to WARNING so the terminal only shows Loki's own activity.
"""

import logging
import sys
from pathlib import Path

# ── ANSI colors (auto-disabled if terminal doesn't support them) ──────────────
class C:
    RESET   = "\033[0m"
    DIM     = "\033[2m"
    BOLD    = "\033[1m"
    GOLD    = "\033[38;5;179m"   # Loki gold
    PURPLE  = "\033[38;5;141m"
    BLUE    = "\033[38;5;75m"
    GREEN   = "\033[38;5;78m"
    RED     = "\033[38;5;203m"
    YELLOW  = "\033[38;5;221m"
    GREY    = "\033[38;5;245m"
    CYAN    = "\033[38;5;80m"


# Short, friendly tags for each module — keeps the left column tidy
_COMPONENT_TAGS = {
    "loki.main":                    ("LOKI ", C.GOLD),
    "loki.core.voice_pipeline":     ("VOICE", C.PURPLE),
    "loki.core.wakeword":           ("WAKE ", C.CYAN),
    "loki.core.listener":           ("HEAR ", C.BLUE),
    "loki.core.conversation_sm":    ("CONV ", C.PURPLE),
    "loki.core.brain":              ("BRAIN", C.GOLD),
    "loki.core.tts":                ("SPEAK", C.GREEN),
    "loki.core.action_router":      ("ROUTE", C.YELLOW),
    "loki.core.audit":              ("AUDIT", C.GREY),
    "loki.ui.server":               ("WEB  ", C.BLUE),
    "loki.features.rag_engine":     ("RAG  ", C.CYAN),
    "loki.features.auto_agent":     ("AGENT", C.PURPLE),
}

_LEVEL_COLORS = {
    "DEBUG":    C.GREY,
    "INFO":     C.RESET,
    "WARNING":  C.YELLOW,
    "ERROR":    C.RED,
    "CRITICAL": C.BOLD + C.RED,
}

# Loggers that flood the terminal with noise — silenced to WARNING
_NOISY_LOGGERS = [
    "httpx", "httpcore", "urllib3", "openai", "comtypes",
    "comtypes.client._code_cache", "asyncio", "websockets",
    "uvicorn.access", "PIL", "numba", "matplotlib",
]


def _force_utf8_stdout() -> bool:
    """Reconfigure stdout to UTF-8 so emojis/box chars don't crash on Windows cp1252.
    Returns True if UTF-8 output is available."""
    try:
        # Python 3.7+ — reconfigure the existing stream in place
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        return True
    except Exception:
        # Older Python or non-reconfigurable stream — check current encoding
        enc = (getattr(sys.stdout, "encoding", "") or "").lower()
        return "utf" in enc


_UTF8_OK = _force_utf8_stdout()


def _supports_color() -> bool:
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


class TerminalFormatter(logging.Formatter):
    """Compact, aligned, color-coded one-line format for the terminal."""

    def __init__(self, use_color: bool):
        super().__init__()
        self._color = use_color

    def format(self, record: logging.LogRecord) -> str:
        if record.name in _COMPONENT_TAGS:
            tag, tag_color = _COMPONENT_TAGS[record.name]
        else:
            # Unmapped logger — use the last module segment, uppercased, padded to 5
            last = record.name.rsplit(".", 1)[-1]
            tag, tag_color = last[:5].upper().ljust(5), C.GREY
        ts = self.formatTime(record, "%H:%M:%S")
        level = record.levelname
        msg = record.getMessage()

        if self._color:
            lvl_color = _LEVEL_COLORS.get(level, C.RESET)
            # [HH:MM:SS] TAG  message
            line = (
                f"{C.DIM}{ts}{C.RESET} "
                f"{tag_color}{C.BOLD}{tag}{C.RESET} "
                f"{lvl_color}{msg}{C.RESET}"
            )
            # Show WARNING/ERROR level inline for visibility
            if level in ("WARNING", "ERROR", "CRITICAL"):
                line = f"{C.DIM}{ts}{C.RESET} {tag_color}{C.BOLD}{tag}{C.RESET} {lvl_color}[{level}] {msg}{C.RESET}"
        else:
            prefix = f"[{level}] " if level != "INFO" else ""
            line = f"{ts} {tag} {prefix}{msg}"

        if record.exc_info:
            line += "\n" + self.formatException(record.exc_info)
        return line


def setup_logging(config: dict, log_path: Path) -> None:
    """Configure root logger with a clean terminal handler + detailed file handler."""
    log_cfg = config.get("logging", {})
    level_name = log_cfg.get("level", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    use_color = _supports_color() and log_cfg.get("color", True)

    log_path.parent.mkdir(parents=True, exist_ok=True)

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)  # capture everything; handlers filter
    root.handlers.clear()

    # ── Terminal handler: clean, color-coded, level-filtered ──
    term = logging.StreamHandler(sys.stdout)
    term.setLevel(level)
    term.setFormatter(TerminalFormatter(use_color))
    root.addHandler(term)

    # ── File handler: full detail, always DEBUG, no color ──
    fileh = logging.FileHandler(log_path, encoding="utf-8")
    fileh.setLevel(logging.DEBUG)
    fileh.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    ))
    root.addHandler(fileh)

    # ── Silence noisy third-party loggers on the terminal ──
    for noisy in _NOISY_LOGGERS:
        logging.getLogger(noisy).setLevel(logging.WARNING)

    logging.getLogger("loki.main").info(
        f"Logging ready — terminal: {level_name}, file: DEBUG → {log_path.name}"
    )


# ── Visual section banners for the terminal ───────────────────────────────────

def banner(text: str, color: str = C.GOLD) -> None:
    """Print a boxed section banner directly to the terminal (bypasses logging)."""
    use_color = _supports_color()
    width = 60
    if _UTF8_OK:
        line = "═" * width
        tl, tr, bl, br, v = "╔", "╗", "╚", "╝", "║"
    else:
        line = "=" * width
        tl, tr, bl, br, v = "+", "+", "+", "+", "|"
    if use_color:
        print(f"{color}{C.BOLD}{tl}{line}{tr}{C.RESET}")
        print(f"{color}{C.BOLD}{v} {text.ljust(width - 1)}{v}{C.RESET}")
        print(f"{color}{C.BOLD}{bl}{line}{br}{C.RESET}")
    else:
        print(f"{tl}{line}{tr}")
        print(f"{v} {text.ljust(width - 1)}{v}")
        print(f"{bl}{line}{br}")


def flow(stage: str, detail: str = "") -> None:
    """Log a voice-pipeline flow transition with a visual arrow marker.
    Use for the big state changes the user wants to watch."""
    logger = logging.getLogger("loki.main")
    arrow = "→"
    msg = f"{arrow} {stage}" + (f": {detail}" if detail else "")
    logger.info(msg)
