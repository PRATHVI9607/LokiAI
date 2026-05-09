#!/usr/bin/env python3
"""
Loki AI Desktop Assistant — Main Entry Point

Elite desktop assistant with Norse personality, voice interface,
50+ features, and comprehensive PC control.
"""

import sys
import logging
import random
from pathlib import Path

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QThread, pyqtSignal, QObject, QTimer
import yaml
from dotenv import load_dotenv

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import Loki core
from loki.core.brain import LokiBrain
from loki.core.listener import SpeechListener
from loki.core.wakeword import WakewordDetector
from loki.core.tts import create_tts_engine
from loki.core.action_router import ActionRouter
from loki.core.undo_stack import UndoStack
from loki.core.memory import MemoryManager

# Import actions
from loki.actions.file_ops import FileOps
from loki.actions.shell_exec import ShellExec
from loki.actions.system_ctrl import SystemCtrl
from loki.actions.app_ctrl import AppCtrl
from loki.actions.browser_ctrl import BrowserCtrl

# Import features
from loki.features.file_search import FileSearch
from loki.features.system_monitor import SystemMonitor
from loki.features.process_manager import ProcessManager
from loki.features.web_summarizer import WebSummarizer
from loki.features.pdf_chat import PDFChat
from loki.features.code_assistant import CodeAssistant
from loki.features.git_helper import GitHelper
from loki.features.focus_mode import FocusMode
from loki.features.task_manager import TaskManager
from loki.features.clipboard_manager import ClipboardManager
from loki.features.vault import Vault
from loki.features.security_scanner import SecurityScanner
from loki.features.file_organizer import FileOrganizer

# Import UI
from loki.ui.main_window import create_loki_window

LOKI_LOG = PROJECT_ROOT / "loki" / "loki.log"


def setup_logging(config: dict) -> None:
    log_cfg = config.get("logging", {})
    level = getattr(logging, log_cfg.get("level", "INFO"), logging.INFO)
    fmt = log_cfg.get("format", "%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    LOKI_LOG.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=level,
        format=fmt,
        handlers=[
            logging.FileHandler(LOKI_LOG, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


logger = logging.getLogger("loki.main")

DISMISSALS = [
    "Farewell. Try not to cause chaos without me.",
    "Until next time. Don't touch anything important.",
    "Gone, but never truly absent.",
]


class ConversationManager(QObject):
    """Orchestrates conversation flow — wakeword → listen → process → respond."""

    _show_signal = pyqtSignal()
    _hide_signal = pyqtSignal()
    _status_signal = pyqtSignal(str)

    def __init__(self, config: dict, window, tts, brain: LokiBrain, router: ActionRouter):
        super().__init__()
        self._cfg = config
        self._window = window
        self._tts = tts
        self._brain = brain
        self._router = router
        self._active = False
        self._timeout_sec = config.get("ui", {}).get("conversation_timeout_seconds", 30)

        self._timer = QTimer()
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._on_timeout)

        self._show_signal.connect(window.show_window)
        self._hide_signal.connect(window.hide_window)
        self._status_signal.connect(window.set_status)

    def start_conversation(self) -> None:
        if self._active:
            self._reset_timer()
            return
        self._active = True
        self._show_signal.emit()
        self._status_signal.emit("listening")
        self._reset_timer()
        logger.info("Conversation started")

    def process_input(self, text: str) -> None:
        if not text or not text.strip():
            return

        self._window.add_user_message(text)
        self._status_signal.emit("thinking")
        self._window.clear_transcript()

        try:
            full_response = ""
            for chunk in self._brain.ask(text):
                full_response += chunk

            if not full_response.strip():
                full_response = "Hmm. That query produced nothing of substance. Try again."

            # Check for JSON intent
            intent = self._brain.parse_intent(full_response)
            if intent and intent.get("intent") and intent["intent"] != "chat":
                self._handle_intent(intent)
            else:
                self._window.add_loki_message(full_response)
                self._speak(full_response)

        except Exception as e:
            logger.error(f"Process input error: {e}", exc_info=True)
            err_msg = "Something went awry. Even gods have bad days."
            self._window.add_loki_message(err_msg)
            self._speak(err_msg)
        finally:
            self._reset_timer()

    def _handle_intent(self, intent: dict) -> None:
        loki_msg = intent.get("message", "")
        if loki_msg:
            self._window.add_loki_message(loki_msg)
            self._speak(loki_msg)

        self._status_signal.emit("thinking")
        result = self._router.route_intent(intent)
        result_msg = result.get("message", "")

        if result_msg and result_msg != loki_msg:
            self._window.add_loki_message(result_msg)
            if result.get("success"):
                self._speak(result_msg)

        if not result.get("success") and not loki_msg:
            fallback = f"That operation failed. {result_msg}"
            self._window.add_loki_message(fallback)
            self._speak(fallback)

        self._status_signal.emit("idle")

    def _speak(self, text: str) -> None:
        self._status_signal.emit("speaking")
        try:
            self._tts.speak(text)
        except Exception as e:
            logger.error(f"TTS error: {e}")
            self._status_signal.emit("idle")

    def _reset_timer(self) -> None:
        self._timer.stop()
        self._timer.start(self._timeout_sec * 1000)

    def _on_timeout(self) -> None:
        if not self._active:
            return
        farewell = random.choice(DISMISSALS)
        self._window.add_loki_message(farewell)
        self._speak(farewell)
        QTimer.singleShot(3000, self._end_conversation)

    def _end_conversation(self) -> None:
        self._active = False
        self._status_signal.emit("idle")
        self._hide_signal.emit()
        logger.info("Conversation ended")


class LokiApplication:
    """Main application coordinator."""

    def __init__(self):
        config_path = PROJECT_ROOT / "loki" / "config.yaml"
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        env_path = PROJECT_ROOT / "loki" / ".env"
        if env_path.exists():
            load_dotenv(env_path)

        setup_logging(self.config)
        logger.info("=" * 60)
        logger.info("  LOKI AI DESKTOP ASSISTANT — Starting up")
        logger.info("=" * 60)

        self.qt_app = QApplication(sys.argv)
        self.qt_app.setApplicationName("Loki")
        self.qt_app.setQuitOnLastWindowClosed(False)

        self._init_all()
        self._wire_signals()

    def _init_all(self) -> None:
        memory_dir = PROJECT_ROOT / "loki" / "memory"

        self.undo_stack = UndoStack(max_depth=self.config.get("undo", {}).get("max_depth", 25))
        self.memory = MemoryManager(memory_dir)
        self.brain = LokiBrain(self.config.get("llm", {}), memory_dir)
        self.tts = create_tts_engine(self.config)
        self.window = create_loki_window(self.config)

        # Actions
        actions_cfg = self.config.get("actions", {})
        self.file_ops = FileOps(self.undo_stack)
        self.shell = ShellExec(actions_cfg, self.undo_stack)
        self.sys_ctrl = SystemCtrl(self.undo_stack)
        self.app_ctrl = AppCtrl()
        self.browser = BrowserCtrl()

        # Features
        feat_cfg = self.config.get("features", {})
        self.file_search = FileSearch(feat_cfg.get("file_search", {}))
        self.sys_monitor = SystemMonitor(feat_cfg.get("system_monitor", {}))
        self.proc_manager = ProcessManager()
        self.web_summarizer = WebSummarizer(brain=self.brain)
        self.pdf_chat = PDFChat(brain=self.brain)
        self.code_assistant = CodeAssistant(brain=self.brain)
        self.git_helper = GitHelper(brain=self.brain)
        self.focus_mode = FocusMode(feat_cfg.get("focus_mode", {}))
        self.task_manager = TaskManager(self.memory)
        self.clipboard = ClipboardManager()
        self.clipboard.start_monitoring()
        self.vault = Vault(memory_dir / "vault.enc")
        self.security_scanner = SecurityScanner(self.config.get("features", {}).get("security_scanner", {}).get("patterns"))
        self.file_organizer = FileOrganizer(feat_cfg.get("file_organizer", {}))

        # Router
        self.router = ActionRouter(self.undo_stack)
        # Register actions
        self.router.register_action("file_ops", self.file_ops)
        self.router.register_action("shell_exec", self.shell)
        self.router.register_action("system_ctrl", self.sys_ctrl)
        self.router.register_action("app_ctrl", self.app_ctrl)
        self.router.register_action("browser_ctrl", self.browser)
        # Register features
        self.router.register_feature("file_search", self.file_search)
        self.router.register_feature("system_monitor", self.sys_monitor)
        self.router.register_feature("process_manager", self.proc_manager)
        self.router.register_feature("web_summarizer", self.web_summarizer)
        self.router.register_feature("pdf_chat", self.pdf_chat)
        self.router.register_feature("code_assistant", self.code_assistant)
        self.router.register_feature("git_helper", self.git_helper)
        self.router.register_feature("focus_mode", self.focus_mode)
        self.router.register_feature("task_manager", self.task_manager)
        self.router.register_feature("clipboard_manager", self.clipboard)
        self.router.register_feature("vault", self.vault)
        self.router.register_feature("security_scanner", self.security_scanner)
        self.router.register_feature("file_organizer", self.file_organizer)

        # Conversation manager
        self.conversation = ConversationManager(
            self.config, self.window, self.tts, self.brain, self.router
        )

        # Audio
        self.listener = SpeechListener(self.config)
        self.wakeword = WakewordDetector(self.config)

        logger.info("All components initialized")

    def _wire_signals(self) -> None:
        # Wakeword → start conversation + listen
        self.wakeword.wakeword_detected.connect(self.conversation.start_conversation)
        self.wakeword.wakeword_detected.connect(self.listener.start_listening)
        self.wakeword.transcript_available.connect(self.window.update_transcript)
        self.wakeword.wakeword_detected.connect(self.window.clear_transcript)

        # Listener → process input
        self.listener.transcript_ready.connect(self.conversation.process_input)

        # Text input → process
        self.window.user_text_submitted.connect(self.conversation.start_conversation)
        self.window.user_text_submitted.connect(self.conversation.process_input)

        # TTS signals
        self.tts.speaking_started.connect(lambda: self.window.set_status("speaking"))
        self.tts.speaking_stopped.connect(lambda: self.window.set_status("idle"))

        # UI signals
        self.window.mute_toggled.connect(self._on_mute)
        self.window.undo_requested.connect(self._on_undo)
        self.window.window_closing.connect(self._on_quit)

        logger.info("Signals connected")

    def _on_mute(self, is_muted: bool) -> None:
        if is_muted:
            self.wakeword.stop()
            self.listener.stop_listening()
        else:
            self.wakeword.start()
            self.window.set_status("idle")

    def _on_undo(self) -> None:
        if self.undo_stack.is_empty():
            self.window.add_loki_message("Nothing to undo. The slate is already clean.")
            return
        success = self.undo_stack.pop_and_undo()
        msg = "Done. Reversed." if success else "Undo failed. Some things are permanent."
        self.window.add_loki_message(msg)

    def _on_quit(self) -> None:
        logger.info("Shutting down Loki...")
        self.wakeword.stop()
        self.listener.stop_listening()
        self.tts.stop()
        self.clipboard.stop_monitoring()

    def run(self) -> int:
        logger.info("Starting wakeword detector...")
        self.wakeword.start()

        name = self.memory.get_user_name()
        self.window.add_system_message(f"Loki online. Welcome back, {name}.")
        logger.info(f"Loki is listening. Say 'Hey Loki' to begin.")

        exit_code = self.qt_app.exec()
        self._on_quit()
        logger.info("Loki shut down.")
        return exit_code


def main() -> None:
    try:
        app = LokiApplication()
        sys.exit(app.run())
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(0)
    except Exception as e:
        logging.critical(f"Fatal startup error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
