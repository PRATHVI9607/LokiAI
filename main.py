#!/usr/bin/env python3
"""
Loki AI Desktop Assistant — Main Entry Point

FastAPI + Next.js UI, voice interface, 50+ features, comprehensive PC control.
"""

import asyncio
import logging
import socket
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
from loki.core.outcome_log import OutcomeLog
from loki.core.bandit import ProviderBandit
from loki.core.voice_pipeline import VoicePipeline
from loki.core.conversation_sm import ConversationStateMachine
from loki.core.log_setup import setup_logging, banner as log_banner, flow as log_flow
from loki.features.rag_engine import RagEngine

from loki.actions.file_ops import FileOps
from loki.actions.shell_exec import ShellExec
from loki.actions.system_ctrl import SystemCtrl
from loki.actions.app_ctrl import AppCtrl
from loki.actions.browser_ctrl import BrowserCtrl
from loki.actions.computer_control import ComputerControl

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

# Remaining / enhancement features
from loki.features.screenshot_search import ScreenshotSearch
from loki.features.calendar_manager import CalendarManager
from loki.features.expense_tracker import ExpenseTracker
from loki.features.dynamic_ui import DynamicUI
from loki.features.file_watcher import FileWatcher
from loki.features.clipboard_sync import ClipboardSync
from loki.features.proactive_monitor import ProactiveMonitor
from loki.features.google_integration import GoogleIntegration
from loki.features.spotify_integration import SpotifyIntegration
from loki.features.second_brain import SecondBrain
from loki.features.auto_agent import AutoAgent

from loki.ui.server import create_loki_server

LOKI_LOG = PROJECT_ROOT / "loki" / "loki.log"

logger = logging.getLogger("loki.main")


def _free_port(port: int) -> None:
    """Kill any process holding the given port so re-runs never fail with EADDRINUSE."""
    try:
        import psutil
        for conn in psutil.net_connections(kind="inet"):
            if conn.laddr.port == port and conn.status == "LISTEN":
                try:
                    psutil.Process(conn.pid).terminate()
                    logger.info(f"Freed port {port} (killed PID {conn.pid})")
                except Exception:
                    pass
    except Exception:
        pass  # psutil unavailable or permission denied — uvicorn will surface the real error


def _verify_ollama(ollama_url: str, timeout: float = 2.0) -> bool:
    """Quick reachability probe for a local Ollama server."""
    try:
        import requests
        return requests.get(f"{ollama_url}/api/tags", timeout=timeout).status_code == 200
    except Exception:
        return False


class LokiApplication:
    """Main application coordinator — FastAPI + uvicorn, no Qt."""

    def __init__(self):
        config_path = PROJECT_ROOT / "loki" / "config.yaml"
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        env_path = PROJECT_ROOT / "loki" / ".env"
        if env_path.exists():
            load_dotenv(env_path)

        setup_logging(self.config, LOKI_LOG)
        log_banner("  LOKI AI DESKTOP ASSISTANT — Starting up")

        self._init_all()
        self._wire_callbacks()

    def _init_all(self) -> None:
        memory_dir = PROJECT_ROOT / "loki" / "memory"

        self.undo_stack = UndoStack(max_depth=self.config.get("undo", {}).get("max_depth", 25))
        self.memory = MemoryManager(memory_dir)

        # KORTEX-inspired components
        self.brain_memory = BrainMemory(memory_dir)
        self.audit_log = AuditLog(memory_dir)
        self.outcome_log = OutcomeLog(memory_dir)  # passive training-data capture (RL step #1)
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
        # Fail-soft startup probe: if prefer_local is on but Ollama isn't up, say so
        # clearly once at startup rather than silently falling back to slower cloud LLMs.
        if self.config.get("llm", {}).get("prefer_local"):
            if _verify_ollama(ollama_url):
                logger.info(f"Ollama reachable at {ollama_url} — local LLM ready")
            else:
                logger.warning(
                    f"Ollama NOT reachable at {ollama_url} — prefer_local is on but Loki "
                    f"will use cloud LLMs (slower). Start it with 'ollama serve'."
                )
        self.rag_engine = RagEngine(memory_dir, ollama_url=ollama_url)

        self.brain = LokiBrain(
            self.config.get("llm", {}),
            memory_dir,
            brain_memory=self.brain_memory,
            rag_engine=self.rag_engine,
        )
        # Learning loop: the bandit reorders cloud providers by learned reward,
        # using the outcome log as its training data. Cold-start = default order.
        _bcfg = self.config.get("llm", {}).get("bandit", {})
        self.bandit = ProviderBandit(
            self.outcome_log,
            epsilon=_bcfg.get("epsilon", 0.15),
            enabled=_bcfg.get("enabled", True),
        )
        self.brain._bandit = self.bandit
        self.tts = create_tts_engine(self.config)
        self.server = create_loki_server(self.config)
        self.server.set_components(
            rag_engine=self.rag_engine,
            brain_memory=self.brain_memory,
            audit_log=self.audit_log,
            uploads_dir=memory_dir / "uploads",
            outcome_log=self.outcome_log,
            bandit=self.bandit,
            brain=self.brain,
        )

        actions_cfg = self.config.get("actions", {})
        self.file_ops = FileOps(self.undo_stack, extra_roots=[Path(__file__).parent])
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
        self.news_aggregator = NewsAggregator()
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
        # Wire KG into brain for context fusion — done after both are initialized
        # (KG needs brain for LLM extraction; brain needs KG for retrieval-time entity lookup)
        self.brain._knowledge_graph = self.knowledge_graph
        self.meeting_transcriber = MeetingTranscriber(brain=self.brain)
        self.footprint_auditor = FootprintAuditor()
        self.browser_history = SemanticBrowserHistory(brain=self.brain)

        # Remaining / enhancement features
        self.screenshot_search = ScreenshotSearch(brain=self.brain)
        self.computer_control = ComputerControl(screenshot_search=self.screenshot_search)
        self.calendar_manager = CalendarManager(brain=self.brain)
        self.expense_tracker = ExpenseTracker(brain=self.brain)
        self.dynamic_ui = DynamicUI()
        self.file_watcher = FileWatcher(
            backup_manager=self.backup_manager,
            media_converter=self.media_converter,
        )
        self.clipboard_sync = ClipboardSync()
        self.auto_agent = AutoAgent(brain=self.brain)
        self.proactive = ProactiveMonitor(
            self.config,
            on_alert=self._on_proactive_alert,
            is_busy=lambda: self.conversation.is_active,
        )
        self.google = GoogleIntegration(memory_dir)
        self.spotify = SpotifyIntegration(memory_dir)
        self.second_brain = SecondBrain(memory_dir, rag_engine=self.rag_engine)

        self.router = ActionRouter(self.undo_stack)
        self.router.register_action("file_ops", self.file_ops)
        self.router.register_action("shell_exec", self.shell)
        self.router.register_action("system_ctrl", self.sys_ctrl)
        self.router.register_action("app_ctrl", self.app_ctrl)
        self.router.register_action("browser_ctrl", self.browser)
        self.router.register_action("computer_control", self.computer_control)
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
        self.router.register_feature("google", self.google)
        self.router.register_feature("spotify", self.spotify)
        self.router.register_feature("second_brain", self.second_brain)
        # Remaining / enhancement features
        self.router.register_feature("screenshot_search", self.screenshot_search)
        self.router.register_feature("calendar_manager", self.calendar_manager)
        self.router.register_feature("expense_tracker", self.expense_tracker)
        self.router.register_feature("dynamic_ui", self.dynamic_ui)
        self.router.register_feature("file_watcher", self.file_watcher)
        self.router.register_feature("clipboard_sync", self.clipboard_sync)
        self.router.register_feature("auto_agent", self.auto_agent)

        # Wire auto_agent router now that router is fully initialized
        self.auto_agent._router = self.router

        # Conversation state machine (replaces ConversationManager)
        self.conversation = ConversationStateMachine(
            self.config, self.server, self.tts, self.brain, self.router,
            self.audit_log, self.outcome_log,
        )

        # Voice pipeline — exclusive mic management (wakeword ↔ listener)
        self.voice = VoicePipeline(
            wakeword=WakewordDetector(self.config),
            listener=SpeechListener(self.config),
        )

        logger.info("All components initialized")

    def _wire_callbacks(self) -> None:
        # VoicePipeline → conversation state machine
        self.voice.on_wakeword = self._on_wakeword
        self.voice.on_transcript = self._on_voice_transcript
        self.voice.on_transcript_partial = self.server.update_transcript

        # ConversationStateMachine → voice pipeline
        self.conversation.on_ready_for_next = self.voice.resume_listening
        self.conversation.on_ended = self.voice.return_to_wakeword

        # TTS done → state machine drives the next transition
        self.tts.on_speaking_stopped = self.conversation.on_tts_done

        # Server (browser UI) → Python
        self.server.on_user_message = self._on_browser_message
        self.server.on_mute_toggle  = lambda m: self.voice.set_muted(m)
        self.server.on_undo         = self._on_undo
        self.server.on_feedback     = self._on_feedback
        self.server.on_stop_speaking = self.conversation.barge_in

        # AutoAgent progress → chat feed
        self.auto_agent._on_progress = self.server.add_loki_message

        logger.info("Callbacks wired")

    # ── Thin event handlers ─────────────────────────────────────────────

    def _on_wakeword(self) -> None:
        self.conversation.start_conversation()
        self.server.clear_transcript()

    def _on_voice_transcript(self, text: str) -> None:
        self.conversation.process_input(text)

    def _on_browser_message(self, text: str) -> None:
        self.conversation.start_conversation()
        self.conversation.process_input(text)

    def _on_undo(self) -> None:
        if self.undo_stack.is_empty():
            self.server.add_loki_message("Nothing to undo. The slate is already clean.")
            return
        success = self.undo_stack.pop_and_undo()
        self.server.add_loki_message("Done. Reversed." if success else "Undo failed. Some things are permanent.")

    def _on_feedback(self, interaction_id: str, rating: str, correction: str = "") -> None:
        """User gave 👍/👎 (and maybe a correction) on a past response — feeds the learning loop."""
        ok = self.outcome_log.record_feedback(interaction_id, rating, correction)
        if ok:
            logger.info(f"📊 feedback recorded: {rating} on {interaction_id}")

    def _on_proactive_alert(self, text: str, speak: bool) -> None:
        """Loki noticed something and is speaking up unprompted."""
        self.server.add_loki_message(text)
        if speak and self.tts.is_idle:
            self.tts.speak(text)

    # ── Lifecycle ───────────────────────────────────────────────────────

    def shutdown(self) -> None:
        logger.info("Shutting down Loki...")
        self.voice.deactivate()
        self.tts.stop()
        self.clipboard.stop_monitoring()
        self.file_watcher.stop_all()
        self.proactive.stop()
        if self.clipboard_sync.is_running():
            self.clipboard_sync.stop()
        if self.auto_agent.is_running():
            self.auto_agent.cancel()
        try:
            self.dynamic_ui.stop_auto_theme()
        except Exception:
            pass

    def run(self) -> None:
        port = self.config.get("ui", {}).get("port", 7777)

        # Activate voice pipeline (wakeword starts)
        self.voice.activate()
        # Start the proactive watcher (unprompted system/time observations)
        self.proactive.start()

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
            loop = asyncio.get_event_loop()
            # Swallow the benign Windows "connection forcibly closed" noise that
            # fires whenever a browser tab refreshes/closes a WebSocket (WinError
            # 10054). It's harmless — just stops it spamming the terminal.
            def _quiet_conn_reset(loop, context):
                exc = context.get("exception")
                if isinstance(exc, (ConnectionResetError, ConnectionAbortedError)):
                    return
                loop.default_exception_handler(context)
            loop.set_exception_handler(_quiet_conn_reset)
            asyncio.create_task(_startup())
            self.server.set_loop(loop)

        self.server.add_startup_handler(on_startup)
        app = self.server.get_app()

        # Open browser after a short delay
        def open_browser():
            import time
            time.sleep(2)
            self.server.open_browser()

        threading.Thread(target=open_browser, daemon=True).start()

        _free_port(port)  # kill any stale Loki instance before binding
        try:
            uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")
        except KeyboardInterrupt:
            pass
        finally:
            self.shutdown()


def main() -> None:
    # --debug / -d flag flips terminal logging to DEBUG (shows wakeword candidates,
    # audio frames, LLM timing, context injection — everything)
    debug = "--debug" in sys.argv or "-d" in sys.argv
    try:
        app = LokiApplication()
        if debug:
            logging.getLogger().handlers[0].setLevel(logging.DEBUG)  # terminal handler
            logger.info("🔍 DEBUG logging enabled — verbose terminal output")
        app.run()
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(0)
    except Exception as e:
        logging.critical(f"Fatal startup error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
