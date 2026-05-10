#!/usr/bin/env python3
"""
Loki AI Desktop Assistant — Main Entry Point

FastAPI + Next.js UI, voice interface, 50+ features, comprehensive PC control.
"""

import asyncio
import logging
import os
import random
import sys
import threading
from pathlib import Path

import uvicorn
import yaml
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from loki.core.brain import LokiBrain
from loki.core.brain_memory import BrainMemory
from loki.core.listener import SpeechListener
from loki.core.wakeword import WakewordDetector
from loki.core.tts import create_tts_engine
from loki.core.action_router import ActionRouter
from loki.core.undo_stack import UndoStack
from loki.core.memory import MemoryManager
from loki.core.audit import AuditLog
from loki.features.rag_engine import RagEngine

from loki.actions.file_ops import FileOps
from loki.actions.shell_exec import ShellExec
from loki.actions.system_ctrl import SystemCtrl
from loki.actions.app_ctrl import AppCtrl
from loki.actions.browser_ctrl import BrowserCtrl

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

# Batch 1 features
from loki.features.ghostwriter import GhostWriter
from loki.features.grammar_polisher import GrammarPolisher
from loki.features.citation_generator import CitationGenerator
from loki.features.email_drafter import EmailDrafter
from loki.features.daily_briefing import DailyBriefing
from loki.features.fact_checker import FactChecker
from loki.features.currency_converter import CurrencyConverter

# Batch 2 features
from loki.features.news_aggregator import NewsAggregator
from loki.features.api_mocker import ApiMocker
from loki.features.env_setup import EnvSetup
from loki.features.media_converter import MediaConverter
from loki.features.digital_declutter import DigitalDeclutter
from loki.features.backup_manager import BackupManager
from loki.features.software_updater import SoftwareUpdater

# Batch 3 features
from loki.features.window_tiler import WindowTiler
from loki.features.process_triage import ProcessTriage
from loki.features.phishing_detector import PhishingDetector
from loki.features.knowledge_graph import KnowledgeGraph
from loki.features.meeting_transcriber import MeetingTranscriber
from loki.features.footprint_auditor import FootprintAuditor
from loki.features.semantic_browser_history import SemanticBrowserHistory

from loki.ui.server import create_loki_server

LOKI_LOG = PROJECT_ROOT / "loki" / "loki.log"

DISMISSALS = [
    "Farewell. Try not to cause chaos without me.",
    "Until next time. Don't touch anything important.",
    "Gone, but never truly absent.",
]


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


class ConversationManager:
    """Orchestrates wakeword → listen → process → respond flow."""

    def __init__(self, config: dict, server, tts, brain: LokiBrain, router: ActionRouter, audit_log=None):
        self._cfg = config
        self._server = server
        self._tts = tts
        self._brain = brain
        self._router = router
        self._audit = audit_log
        self._active = False
        self._timeout_sec = config.get("ui", {}).get("conversation_timeout_seconds", 30)
        self._timeout_handle = None

    def _reset_timeout(self) -> None:
        if self._timeout_handle:
            self._timeout_handle.cancel()
        loop = asyncio.get_event_loop()
        self._timeout_handle = loop.call_later(self._timeout_sec, self._on_timeout)

    def _on_timeout(self) -> None:
        if not self._active:
            return
        farewell = random.choice(DISMISSALS)
        self._server.add_loki_message(farewell)
        self._speak(farewell)
        threading.Timer(3.0, self._end_conversation).start()

    def start_conversation(self) -> None:
        if self._active:
            self._reset_timeout()
            return
        self._active = True
        self._server.show_window()
        self._server.set_status("listening")
        self._reset_timeout()
        logger.info("Conversation started")

    def process_input(self, text: str) -> None:
        if not text or not text.strip():
            return

        self._server.add_user_message(text)
        self._server.set_status("thinking")
        self._server.clear_transcript()

        try:
            full_response = ""
            for chunk in self._brain.ask(text):
                full_response += chunk

            if not full_response.strip():
                full_response = "Hmm. That query produced nothing of substance. Try again."

            intent = self._brain.parse_intent(full_response)
            if intent and intent.get("intent") and intent["intent"] != "chat":
                self._handle_intent(intent)
            else:
                self._server.add_loki_message(full_response)
                self._speak(full_response)

        except Exception as e:
            logger.error(f"Process input error: {e}", exc_info=True)
            err_msg = "Something went awry. Even gods have bad days."
            self._server.add_loki_message(err_msg)
            self._speak(err_msg)
        finally:
            self._reset_timeout()

    def _handle_intent(self, intent: dict) -> None:
        loki_msg = intent.get("message", "")
        if loki_msg:
            self._server.add_loki_message(loki_msg)
            self._speak(loki_msg)

        self._server.set_status("thinking")
        result = self._router.route_intent(intent)
        result_msg = result.get("message", "")

        # Audit log
        if self._audit:
            self._audit.log(
                intent=intent.get("intent", "unknown"),
                params=intent.get("params", {}),
                success=result.get("success", False),
                result_summary=result_msg,
            )

        if result_msg and result_msg != loki_msg:
            self._server.add_loki_message(result_msg)
            if result.get("success"):
                self._speak(result_msg)

        if not result.get("success") and not loki_msg:
            fallback = f"That operation failed. {result_msg}"
            self._server.add_loki_message(fallback)
            self._speak(fallback)

        self._server.set_status("idle")

    def _speak(self, text: str) -> None:
        self._server.set_status("speaking")
        try:
            self._tts.speak(text)
        except Exception as e:
            logger.error(f"TTS error: {e}")
            self._server.set_status("idle")

    def _end_conversation(self) -> None:
        self._active = False
        if self._timeout_handle:
            self._timeout_handle.cancel()
        self._server.set_status("idle")
        self._server.hide_window()
        logger.info("Conversation ended")


class LokiApplication:
    """Main application coordinator — FastAPI + uvicorn, no Qt."""

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

        self._init_all()
        self._wire_callbacks()

    def _init_all(self) -> None:
        memory_dir = PROJECT_ROOT / "loki" / "memory"

        self.undo_stack = UndoStack(max_depth=self.config.get("undo", {}).get("max_depth", 25))
        self.memory = MemoryManager(memory_dir)

        # KORTEX-inspired components
        self.brain_memory = BrainMemory(memory_dir)
        self.audit_log = AuditLog(memory_dir)
        llm_port = self.config.get("llm", {}).get("ollama_port")
        wakeword_port = self.config.get("wakeword", {}).get("ollama_port")
        if llm_port is not None:
            ollama_port = llm_port
        elif wakeword_port is not None:
            logger.warning("'wakeword.ollama_port' is deprecated; move it to 'llm.ollama_port'")
            ollama_port = wakeword_port
        else:
            ollama_port = 11434
        ollama_url = f"http://localhost:{ollama_port}"
        self.rag_engine = RagEngine(memory_dir, ollama_url=ollama_url)

        self.brain = LokiBrain(
            self.config.get("llm", {}),
            memory_dir,
            brain_memory=self.brain_memory,
            rag_engine=self.rag_engine,
        )
        self.tts = create_tts_engine(self.config)
        self.server = create_loki_server(self.config)
        self.server.set_components(
            rag_engine=self.rag_engine,
            brain_memory=self.brain_memory,
            audit_log=self.audit_log,
            uploads_dir=memory_dir / "uploads",
        )

        actions_cfg = self.config.get("actions", {})
        self.file_ops = FileOps(self.undo_stack)
        self.shell = ShellExec(actions_cfg, self.undo_stack)
        self.sys_ctrl = SystemCtrl(self.undo_stack)
        self.app_ctrl = AppCtrl()
        self.browser = BrowserCtrl()

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
        scanner_cfg = (self.config.get("features") or {}).get("security_scanner") or {}
        self.security_scanner = SecurityScanner(scanner_cfg.get("patterns"))
        self.file_organizer = FileOrganizer(feat_cfg.get("file_organizer", {}))

        # Batch 1 features
        self.ghostwriter = GhostWriter(brain=self.brain)
        self.grammar_polisher = GrammarPolisher(brain=self.brain)
        self.citation_generator = CitationGenerator(brain=self.brain)
        self.email_drafter = EmailDrafter(brain=self.brain)
        self.fact_checker = FactChecker(brain=self.brain)
        self.currency_converter = CurrencyConverter(brain=self.brain)

        # Batch 2 features
        self.news_aggregator = NewsAggregator(brain=self.brain)
        self.daily_briefing = DailyBriefing(
            brain=self.brain,
            task_manager=self.task_manager,
            system_monitor=self.sys_monitor,
            news_aggregator=self.news_aggregator,
        )
        self.api_mocker = ApiMocker(brain=self.brain)
        self.env_setup = EnvSetup(brain=self.brain)
        self.media_converter = MediaConverter()
        self.digital_declutter = DigitalDeclutter()
        self.backup_manager = BackupManager()
        self.software_updater = SoftwareUpdater()

        # Batch 3 features
        self.window_tiler = WindowTiler()
        self.process_triage = ProcessTriage()
        self.phishing_detector = PhishingDetector(brain=self.brain)
        self.knowledge_graph = KnowledgeGraph(brain=self.brain)
        self.meeting_transcriber = MeetingTranscriber(brain=self.brain)
        self.footprint_auditor = FootprintAuditor()
        self.browser_history = SemanticBrowserHistory(brain=self.brain)

        self.router = ActionRouter(self.undo_stack)
        self.router.register_action("file_ops", self.file_ops)
        self.router.register_action("shell_exec", self.shell)
        self.router.register_action("system_ctrl", self.sys_ctrl)
        self.router.register_action("app_ctrl", self.app_ctrl)
        self.router.register_action("browser_ctrl", self.browser)
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
        # Batch 1
        self.router.register_feature("ghostwriter", self.ghostwriter)
        self.router.register_feature("grammar_polisher", self.grammar_polisher)
        self.router.register_feature("citation_generator", self.citation_generator)
        self.router.register_feature("email_drafter", self.email_drafter)
        self.router.register_feature("fact_checker", self.fact_checker)
        self.router.register_feature("currency_converter", self.currency_converter)
        # Batch 2
        self.router.register_feature("news_aggregator", self.news_aggregator)
        self.router.register_feature("daily_briefing", self.daily_briefing)
        self.router.register_feature("api_mocker", self.api_mocker)
        self.router.register_feature("env_setup", self.env_setup)
        self.router.register_feature("media_converter", self.media_converter)
        self.router.register_feature("digital_declutter", self.digital_declutter)
        self.router.register_feature("backup_manager", self.backup_manager)
        self.router.register_feature("software_updater", self.software_updater)
        # Batch 3
        self.router.register_feature("window_tiler", self.window_tiler)
        self.router.register_feature("process_triage", self.process_triage)
        self.router.register_feature("phishing_detector", self.phishing_detector)
        self.router.register_feature("knowledge_graph", self.knowledge_graph)
        self.router.register_feature("meeting_transcriber", self.meeting_transcriber)
        self.router.register_feature("footprint_auditor", self.footprint_auditor)
        self.router.register_feature("browser_history", self.browser_history)

        self.conversation = ConversationManager(
            self.config, self.server, self.tts, self.brain, self.router, self.audit_log
        )

        self.listener = SpeechListener(self.config)
        self.wakeword = WakewordDetector(self.config)

        logger.info("All components initialized")

    def _wire_callbacks(self) -> None:
        # Wakeword callbacks
        self.wakeword.on_wakeword = self._on_wakeword
        self.wakeword.on_transcript = self.server.update_transcript

        # Listener callbacks
        self.listener.on_transcript = self.conversation.process_input

        # TTS callbacks
        self.tts.on_speaking_started = lambda: self.server.set_status("speaking")
        self.tts.on_speaking_stopped = lambda: self.server.set_status("idle")

        # Server (browser UI) → Python callbacks
        self.server.on_user_message = self._on_browser_message
        self.server.on_mute_toggle = self._on_mute
        self.server.on_undo = self._on_undo

        logger.info("Callbacks wired")

    def _on_wakeword(self) -> None:
        self.conversation.start_conversation()
        self.listener.start_listening()
        self.server.clear_transcript()

    def _on_browser_message(self, text: str) -> None:
        self.conversation.start_conversation()
        self.conversation.process_input(text)

    def _on_mute(self, is_muted: bool) -> None:
        if is_muted:
            self.wakeword.stop()
            self.listener.stop_listening()
        else:
            self.wakeword.start()
            self.server.set_status("idle")

    def _on_undo(self) -> None:
        if self.undo_stack.is_empty():
            self.server.add_loki_message("Nothing to undo. The slate is already clean.")
            return
        success = self.undo_stack.pop_and_undo()
        msg = "Done. Reversed." if success else "Undo failed. Some things are permanent."
        self.server.add_loki_message(msg)

    def shutdown(self) -> None:
        logger.info("Shutting down Loki...")
        self.wakeword.stop()
        self.listener.stop_listening()
        self.tts.stop()
        self.clipboard.stop_monitoring()

    def run(self) -> None:
        port = self.config.get("ui", {}).get("port", 7777)

        # Start wakeword on a background thread
        self.wakeword.start()

        name = self.memory.get_user_name()
        logger.info(f"Loki online. Welcome back, {name}.")
        logger.info(f"Open http://localhost:{port} in your browser.")

        # Give uvicorn the event loop so server can broadcast from threads
        async def _startup():
            self.server.set_loop(asyncio.get_event_loop())
            # Brief delay so browser can connect before the welcome message
            await asyncio.sleep(1.5)
            self.server.add_system_message(f"Loki online. Welcome back, {name}.")
            self.server.set_status("idle")

        async def on_startup():
            asyncio.create_task(_startup())
            self.server.set_loop(asyncio.get_event_loop())

        self.server.add_startup_handler(on_startup)
        app = self.server.get_app()

        # Open browser after a short delay
        def open_browser():
            import time
            time.sleep(2)
            self.server.open_browser()

        threading.Thread(target=open_browser, daemon=True).start()

        try:
            uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")
        except KeyboardInterrupt:
            pass
        finally:
            self.shutdown()


def main() -> None:
    try:
        app = LokiApplication()
        app.run()
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(0)
    except Exception as e:
        logging.critical(f"Fatal startup error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
