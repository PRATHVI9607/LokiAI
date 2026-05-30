"""
Loki's brain — LLM integration with KORTEX-style context engineering.

LLM priority (in order):
  1. Kimi K2  (Moonshot API — fastest, smartest primary)
  2. OpenRouter (cloud fallback)
  3. Ollama    (local fallback)

Context layers (assembled every request):
  1. System prompt — personality + intent catalog
  2. Brain memory  — key facts, decisions, session summaries
  3. Knowledge Graph — entity relationships matching the query (structured)
  4. RAG context   — ChromaDB semantic chunks from indexed files
  5. Chat history  — last N turns
  6. User message

Auto-compression: oldest turns summarized and stored in brain_memory.
Fact extraction: every 5 exchanges, facts extracted and persisted.
"""

import os
import json
import logging
import random
import re
import threading
import time
from typing import Dict, Any, List, Optional, Generator
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

logger = logging.getLogger(__name__)

# ─── Intent catalog ───────────────────────────────────────────────────────────

INTENT_CATALOG = """

# ACTION MODE — CRITICAL
You are NOT a chatbot that explains how to do things. You CONTROL this Windows PC directly.
When the user asks you to DO anything on the computer (open/close apps, set volume/brightness,
manage files, run a search, check the system, etc.), you MUST reply with ONLY a single JSON
object — no prose before or after, no markdown fence, no explanation:

{"intent": "<intent_name>", "params": {...}, "message": "<short in-character acknowledgment>"}

NEVER explain how the user could do it themselves. NEVER say "you can open it by..." or "I can't".
If an intent below matches, EMIT THE JSON. You can actually perform it.

EXAMPLES (follow this exactly):
User: open calculator          → {"intent": "app_open", "params": {"name": "calculator"}, "message": "Opening calculator."}
User: open chrome              → {"intent": "app_open", "params": {"name": "chrome"}, "message": "Launching Chrome."}
User: close notepad            → {"intent": "app_close", "params": {"name": "notepad"}, "message": "Closing notepad."}
User: what is my volume        → {"intent": "volume_get", "params": {}, "message": "Checking volume."}
User: set volume to 30         → {"intent": "volume_set", "params": {"percent": 30}, "message": "Volume to 30%."}
User: dim the screen to 40     → {"intent": "brightness_set", "params": {"percent": 40}, "message": "Brightness to 40%."}
User: how's my system / cpu    → {"intent": "system_monitor", "params": {}, "message": "Reading system stats."}
User: list running processes   → {"intent": "process_list", "params": {}, "message": "Listing processes."}
User: search the web for x     → {"intent": "browser_search", "params": {"query": "x"}, "message": "Searching."}
User: open youtube.com         → {"intent": "browser_open", "params": {"url": "youtube.com"}, "message": "Opening it."}

Only for genuine conversation (greetings, questions, banter) do you reply as plain text in character.

INTENTS (file operations):
- file_create: params={path, content?}
- file_delete: params={path}
- file_move: params={src, dst}
- file_read: params={path}
- folder_create: params={path}
- folder_delete: params={path}
- file_search: params={query, directory?, type?}
- file_organize: params={directory?}

INTENTS (system):
- shell: params={command}
- volume_set: params={percent}
- volume_get: params={}
- brightness_set: params={percent}
- brightness_get: params={}
- wifi_toggle: params={}
- bluetooth_toggle: params={}
- app_open: params={name}
- app_close: params={name}
- browser_open: params={url}
- browser_search: params={query, engine?}
- system_monitor: params={metrics?}
- process_kill: params={name_or_pid}
- process_list: params={}

INTENTS (intelligence):
- web_summarize: params={url}
- pdf_chat: params={path, question}
- code_analyze: params={path}
- code_convert: params={path, from_lang, to_lang}
- commit_message: params={repo_path?}
- readme_generate: params={repo_path?}
- regex_generate: params={description}
- sql_build: params={description, schema?}
- git_status: params={repo_path?}
- git_commit: params={message, repo_path?}
- security_scan: params={path}

INTENTS (productivity):
- focus_mode_enable: params={duration_minutes?}
- focus_mode_disable: params={}
- task_add: params={title, priority?, due?}
- task_list: params={filter?}
- task_complete: params={id}
- task_delete: params={id}
- clipboard_show: params={}
- clipboard_clear: params={}
- vault_store: params={key, value}
- vault_retrieve: params={key}

INTENTS (writing & text):
- text_expand: params={text}
- text_continue: params={text}
- text_bullets_to_prose: params={text}
- text_polish: params={text}
- text_change_tone: params={text, tone}
- text_translate: params={text, language}
- citation_from_url: params={url, style?}
- citation_from_info: params={info, style?}
- email_draft: params={to?, subject, context}
- email_reply: params={original, intent?}
- fact_check: params={claim}
- daily_briefing: params={}

INTENTS (data & conversion):
- currency_convert: params={amount, from_currency, to_currency}
- unit_convert: params={amount, from_unit, to_unit}
- news_headlines: params={topic?, count?}
- news_briefing: params={topics?}
- media_convert: params={input_path, output_format, output_path?, quality?}
- media_info: params={file_path}

INTENTS (software & environment):
- update_check: params={}
- update_all: params={}
- update_package: params={package_name}
- install_package: params={package_name}
- env_dockerfile: params={project_path?}
- env_venv: params={project_path?, python?}
- env_compose: params={project_path?, services?}
- api_mock_generate: params={description}
- api_mock_data: params={schema}

INTENTS (file management):
- backup_file: params={path, destination?}
- backup_directory: params={path, destination?}
- backup_list: params={name_filter?}
- declutter_duplicates: params={directory?}
- declutter_large: params={directory?, threshold_mb?}
- declutter_old: params={directory?, days?}
- declutter_suggest: params={directory?}

INTENTS (window & process):
- window_snap: params={layout, window_title?}
- window_tile_all: params={}
- window_layouts: params={}
- process_analyze: params={top_n?}
- process_triage: params={app_name, dry_run?}
- process_suspend: params={name_or_pid}
- process_resume: params={name_or_pid}

INTENTS (security & privacy):
- phishing_url: params={url}
- phishing_email: params={email_text}
- footprint_startup: params={}
- footprint_tasks: params={}
- footprint_privacy: params={}
- footprint_network: params={}
- footprint_full: params={}

INTENTS (knowledge & history):
- kg_ingest_file: params={file_path}
- kg_ingest_dir: params={directory}
- kg_query: params={question}
- kg_connections: params={entity}
- kg_stats: params={}
- history_search: params={query, browser?, days?}
- history_semantic: params={query, browser?, days?}
- history_recent: params={browser?, days?}
- history_stats: params={browser?}

INTENTS (meetings):
- meeting_transcribe: params={audio_path, language?}
- meeting_minutes: params={audio_path, language?}
- meeting_action_items: params={text_or_path}
- meeting_summarize: params={transcript}

INTENTS (screen & visual):
- screen_capture: params={region?}
- screen_ask: params={question}  (LOOK at the screen and answer — "what's this error", "what's on my screen", "summarize this page")
- screen_read: params={region?}
- screen_search: params={query}
- screen_describe: params={}
- screen_translate: params={target_language?}
- screenshot_save: params={output_path?}

INTENTS (calendar):
- calendar_list: params={days?, ics_path?}
- calendar_conflicts: params={ics_path?}
- calendar_suggest_slot: params={event_title, duration_minutes?, ics_path?}
- calendar_import: params={ics_path}

INTENTS (Google — live Gmail + Calendar of the user's real account):
- calendar_today: params={days?}  ("what's on my calendar", "my schedule today", "what do I have on")
- calendar_next: params={}        ("what's my next meeting", "when's my next event")
- email_unread: params={count?}   ("any new email", "unread mail", "check my inbox")
- email_send: params={to, subject, body}   ("email alice@x.com saying I'll be late")
- calendar_create: params={title, start, duration_minutes?}   start MUST be ISO 8601 like 2026-06-01T15:00 ("add a meeting tomorrow 3pm called Standup")

INTENTS (Spotify — playback):
- spotify_now: params={}          ("what's playing")
- spotify_play: params={query?}   (query → search & play that; empty → resume)
- spotify_pause: params={}        | spotify_next: params={} | spotify_previous: params={}

INTENTS (second brain — the user's personal long-term memory):
- remember: params={text}         ("remember that my flight is at 6am")
- recall: params={query}          ("what did I say about my flight")
- forget: params={query}          | notes_list: params={}

INTENTS (expenses):
- expense_extract: params={text}
- expense_from_file: params={file_path}
- expense_scan_folder: params={folder}
- expense_list: params={month?}
- expense_summary: params={}

INTENTS (dynamic UI):
- ui_theme_time: params={}
- ui_theme_mood: params={mood}
- ui_wallpaper: params={image_path}
- ui_auto_theme_start: params={}
- ui_auto_theme_stop: params={}
- ui_list_themes: params={}

INTENTS (file watcher):
- watch_backup: params={path, destination?, poll_seconds?}
- watch_media_inbox: params={inbox_dir, output_format?}
- watch_list: params={}
- watch_stop: params={path}

INTENTS (clipboard sync):
- clipboard_sync_start: params={}
- clipboard_sync_stop: params={}
- clipboard_sync_url: params={}
- clipboard_get: params={}
- clipboard_set: params={text}

INTENTS (code refactoring):
- code_refactor: params={path}

INTENTS (task AI prioritize):
- task_prioritize_ai: params={}

INTENTS (deepfake detection):
- deepfake_check: params={file_path}

INTENTS (confirmation / safety):
- confirm_action: params={token?}  (user confirmed a pending destructive action)
- cancel_action: params={}  (user cancelled pending action)

INTENTS (autonomous agent):
- agent_run: params={goal}  (execute a multi-step task autonomously)
- agent_cancel: params={}  (abort running agent task)
- agent_status: params={}  (check if agent is running)

INTENTS (computer control — operate the machine like a person):
- computer_type: params={text}  (type text into the focused window)
- computer_press: params={key}  (a key or hotkey: "enter", "ctrl+s", "alt+tab")
- computer_scroll: params={amount}  (negative = down, positive = up)
- computer_click: params={x?, y?, button?, double?}  (click at coords or current pos)
- computer_click_text: params={target}  (find on-screen text and click it)
- computer_action: params={action}  (minimize, maximize, show desktop, switch window,
  close window, lock, copy, paste, save, select all, new tab, close tab, screenshot)
  (to read the screen, use screen_read from the Screen & Visual section)

INTENTS (misc):
- undo: params={}
- chat: params={}  (no action, pure conversation)

SECURITY RULES:
- Destructive ops (file_delete, folder_delete, process_kill, shell, git_commit, install_package, update_all)
  are automatically held for confirmation — you do NOT need to ask twice; route them normally.
- Never reveal vault contents in the message field.
- Validate that file paths seem reasonable before confirming.
- For agent_run, extract the goal from the user's message (strip "agent:" prefix if present).

For pure conversation (no action needed), respond naturally without JSON — stay in character."""

WAKEWORD_RESPONSES = [
    "At your service. What requires my attention?",
    "You called. I answered. What is it?",
    "I'm here. Make it interesting.",
    "Speak. I'm listening.",
    "The god of mischief awaits your command.",
]

DISMISSAL_MESSAGES = [
    "Farewell. Try not to cause chaos without me.",
    "I'll be here. Scheming.",
    "Until next time. Don't touch anything important.",
    "Gone, but never truly absent.",
]

COMPRESSION_THRESHOLD = 40
COMPRESSION_BATCH = 20
FACT_EXTRACT_EVERY = 5


class LokiBrain:
    """
    LLM integration with KORTEX-style context engineering.

    Provider priority (speed-first):
      1. OpenRouter fast models  ← primary for all real-time voice queries
      2. NVIDIA NIM Kimi K2.6    ← optional deep-reasoning (thinking=False for speed)
      3. Kimi Moonshot direct     ← if KIMI_API_KEY set
      4. Ollama local             ← offline fallback

    Context layers: personality + brain memory + KG entities + RAG chunks + history.
    """

    NVIDIA_NIM_URL = "https://integrate.api.nvidia.com/v1"
    NVIDIA_MODEL   = "moonshotai/kimi-k2.6"

    def __init__(
        self,
        config: dict,
        memory_dir: Path,
        brain_memory=None,
        rag_engine=None,
        knowledge_graph=None,
    ):
        if OpenAI is None:
            raise ImportError("openai package required: pip install openai")

        self._config = config
        self._memory_dir = Path(memory_dir)
        self._brain_memory = brain_memory
        self._rag_engine = rag_engine
        self._knowledge_graph = knowledge_graph

        self._max_tokens = config.get("max_tokens", 600)
        self._temperature = config.get("temperature", 0.70)
        self._max_turns = config.get("max_turns", 20)
        self._prefer_local = config.get("prefer_local", False)  # try Ollama first when reachable
        # thinking=True adds 30–90s latency — off by default for voice assistant
        self._nvidia_thinking = config.get("nvidia_thinking", False)

        # ─── Provider 1 (PRIMARY): OpenRouter — fast free models ──────────────
        self._openrouter_client: Optional[Any] = None
        or_key = os.getenv("OPENROUTER_API_KEY", "")
        if or_key and or_key not in ("your_openrouter_api_key_here", ""):
            try:
                self._openrouter_client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=or_key,
                    timeout=30.0,   # fast models: 30s is plenty
                )
                logger.info("OpenRouter configured (primary fast provider)")
            except Exception as e:
                logger.warning(f"OpenRouter init failed: {e}")
        else:
            logger.warning("OPENROUTER_API_KEY not set")

        # Ordered by verified speed: fastest-working first
        self._fast_models = [
            config.get("fast_model",        "openai/gpt-oss-120b:free"),
            config.get("fallback_model",     "google/gemma-4-31b-it:free"),
            config.get("second_fallback_model", "liquid/lfm-2.5-1.2b-instruct:free"),
        ]
        # vision model for "look at my screen" (multimodal, via OpenRouter)
        self._vision_models = [
            config.get("vision_model", "meta-llama/llama-3.2-11b-vision-instruct:free"),
            "google/gemma-3-27b-it:free",
        ]

        # ─── Provider 2 (DEEP REASONING): NVIDIA NIM — Kimi K2.6 ────────────
        # Only used when thinking=True in config — too slow for real-time voice.
        self._nvidia_client: Optional[Any] = None
        nvidia_key = os.getenv("NVIDIA_API_KEY", "")
        if nvidia_key and not nvidia_key.startswith("your_"):
            try:
                self._nvidia_client = OpenAI(
                    base_url=self.NVIDIA_NIM_URL,
                    api_key=nvidia_key,
                    timeout=18.0,   # fail-fast to OpenRouter if NIM is slow/unreachable
                    max_retries=0,
                )
                mode = "thinking ON" if self._nvidia_thinking else "thinking OFF (fast mode)"
                logger.info(f"NVIDIA NIM configured: {self.NVIDIA_MODEL} ({mode})")
            except Exception as e:
                logger.warning(f"NVIDIA NIM init failed: {e}")
        else:
            logger.info("NVIDIA_API_KEY not set — NVIDIA NIM disabled")

        # ─── Provider 3: Kimi K2 (Moonshot direct API) ───────────────────────
        self._kimi_client: Optional[Any] = None
        self._kimi_model = config.get("kimi_model", "kimi-k2")
        kimi_key = os.getenv("KIMI_API_KEY", "")
        if kimi_key and kimi_key not in ("your_kimi_api_key_here", ""):
            try:
                self._kimi_client = OpenAI(
                    base_url="https://api.moonshot.cn/v1",
                    api_key=kimi_key,
                    timeout=60.0,
                    max_retries=0,
                )
                logger.info(f"Kimi K2 (Moonshot) configured: {self._kimi_model}")
            except Exception as e:
                logger.warning(f"Kimi K2 init failed: {e}")
        else:
            logger.info("Moonshot direct API not set (optional — Kimi K2.6 already served via NVIDIA NIM)")

        # ─── Provider 3: Ollama (local) ────────────────────────────────────────
        self._ollama_infer_client: Optional[Any] = None
        self._ollama_model = config.get("ollama_model", "phi3:mini")
        self._ollama_fallback_model = config.get("ollama_fallback_model", "")
        self._ollama_available = False
        try:
            probe = OpenAI(
                base_url="http://localhost:11434/v1",
                api_key="ollama",
                timeout=3.0,
                max_retries=0,
            )
            probe.models.list()
            self._ollama_timeout = config.get("ollama_timeout", 60)  # voice can't wait 2min
            self._ollama_infer_client = OpenAI(
                base_url="http://localhost:11434/v1",
                api_key="ollama",
                timeout=float(self._ollama_timeout),
                max_retries=0,
            )
            self._ollama_available = True
            logger.info(f"Ollama connected: {self._ollama_model} (timeout {self._ollama_timeout}s)")
        except Exception:
            logger.info("Ollama not running — local inference disabled")

        self._conversation_file = self._memory_dir / "conversation.json"
        self._conversation_history: List[Dict[str, str]] = []
        self._exchange_count = 0
        self._history_lock = threading.Lock()  # guards _conversation_history mutations
        self._maint_running = False            # prevents overlapping maintenance runs
        self.last_provider = "none"            # which provider answered the last query
                                               # (for the outcome logger / future bandit)
        self._bandit = None                    # ProviderBandit, injected by main.py —
                                               # reorders cloud providers by learned reward

        self._load_history()
        self._log_provider_status()

        # Warm up the local model in the background so the first real query is fast
        # (a cold 7B model takes ~20-30s to load into VRAM; warming hides that).
        if self._prefer_local and self._ollama_available:
            threading.Thread(target=self._warmup_ollama, daemon=True, name="loki-ollama-warmup").start()

    def _warmup_ollama(self) -> None:
        try:
            logger.info(f"warming up {self._ollama_model}…")
            t0 = time.time()
            self._ollama_infer_client.chat.completions.create(
                model=self._ollama_model,
                messages=[{"role": "user", "content": "hi"}],
                max_tokens=1,
            )
            logger.info(f"{self._ollama_model} warm and ready ({time.time() - t0:.0f}s)")
        except Exception as e:
            logger.debug(f"Ollama warmup skipped: {e}")

    def _log_provider_status(self) -> None:
        if self._prefer_local and self._ollama_available:
            primary = f"Ollama LOCAL ({self._ollama_model}) → cloud fallback"
        elif self._nvidia_client:
            primary = f"NVIDIA NIM Kimi K2.6 → fallback: OpenRouter ({self._fast_models[0]})"
        elif self._openrouter_client:
            primary = f"OpenRouter → {self._fast_models[0]}"
        elif self._kimi_client:
            primary = f"Kimi Moonshot ({self._kimi_model})"
        else:
            primary = "Ollama (local)"
        logger.info(f"Brain active — {primary}")

    # ─── History ──────────────────────────────────────────────────────────────

    def _load_history(self) -> None:
        if self._conversation_file.exists():
            try:
                with open(self._conversation_file, "r", encoding="utf-8") as f:
                    self._conversation_history = json.load(f)
                logger.info(f"Loaded {len(self._conversation_history)} conversation messages")
            except Exception as e:
                logger.error(f"Failed to load conversation: {e}")
                self._conversation_history = []

    def _save_history(self) -> None:
        self._memory_dir.mkdir(parents=True, exist_ok=True)
        with self._history_lock:
            snapshot = list(self._conversation_history[-(self._max_turns * 2):])
        try:
            with open(self._conversation_file, "w", encoding="utf-8") as f:
                json.dump(snapshot, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save conversation: {e}")

    # ─── Context assembly ─────────────────────────────────────────────────────

    def _build_system_prompt(self) -> str:
        if self._brain_memory:
            personality_prompt = self._brain_memory.get_personality_prompt()
        else:
            from loki.core.brain_memory import PERSONALITY_PROMPTS
            personality_prompt = PERSONALITY_PROMPTS["loki"]

        # Structure: personality (dominant) → user memory → action catalog (last)
        # Personality MUST come first and be visually prominent so smaller models follow it.
        sections = [personality_prompt]

        if self._brain_memory:
            memory_ctx = self._brain_memory.get_memory_context()
            if memory_ctx:
                sections.append(f"## USER CONTEXT\n{memory_ctx}")

        sections.append(INTENT_CATALOG)

        return "\n\n".join(sections)

    def _get_kg_context(self, user_message: str) -> str:
        """Layer 3: knowledge graph entity lookup — structured relational context."""
        if not self._knowledge_graph:
            return ""
        try:
            return self._knowledge_graph.query_entities(user_message)
        except Exception as e:
            logger.warning(f"KG context failed: {e}")
            return ""

    def _get_rag_context(self, user_message: str) -> str:
        """Layer 4: ChromaDB semantic chunks from indexed files."""
        if not self._rag_engine or not self._rag_engine.is_available:
            return ""
        results = self._rag_engine.query(user_message, top_k=6)
        if not results:
            return ""
        return self._rag_engine.format_context(results)

    def _build_messages(
        self,
        user_message: str,
        kg_context: str = "",
        rag_context: str = "",
    ) -> List[Dict[str, str]]:
        """
        Assemble context in priority order:
        1. System prompt (personality + brain memory)
        2. KG entities (structured relational context)
        3. RAG chunks (semantic file context)
        4. Chat history
        5. User message
        """
        messages: List[Dict[str, str]] = [
            {"role": "system", "content": self._build_system_prompt()}
        ]

        if kg_context:
            messages.append({"role": "system", "content": kg_context})

        if rag_context:
            messages.append({"role": "system", "content": rag_context})

        with self._history_lock:
            recent = list(self._conversation_history[-(self._max_turns * 2):])
        messages.extend(recent)
        messages.append({"role": "user", "content": user_message})
        return messages

    # ─── Inference ────────────────────────────────────────────────────────────

    def _call_ollama(self, messages: List[Dict], mt: int) -> str:
        """Call the local Ollama model. Returns '' on failure."""
        if not (self._ollama_available and self._ollama_infer_client):
            return ""
        # Try the primary model; on slowness/failure fall back to the smaller,
        # GPU-resident model (fits fully in 4GB VRAM → fast).
        models = [self._ollama_model]
        if self._ollama_fallback_model and self._ollama_fallback_model != self._ollama_model:
            models.append(self._ollama_fallback_model)
        for model in models:
            try:
                resp = self._ollama_infer_client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=mt,
                    temperature=self._temperature,
                    extra_body={"keep_alive": "30m"},  # keep model in VRAM between turns
                )
                text = resp.choices[0].message.content or ""
                if text.strip():
                    logger.debug(f"Response from Ollama ({model})")
                    return text
            except Exception as e:
                logger.warning(f"Ollama {model}: {e}")
        return ""

    # ── individual provider calls (each returns text or "") ──────────────────

    def _try_nvidia(self, messages: List[Dict], mt: int) -> str:
        if not self._nvidia_client:
            return ""
        try:
            extra: dict = {}
            timeout_override = 60.0
            if self._nvidia_thinking:
                extra = {"chat_template_kwargs": {"thinking": True}}
                timeout_override = 180.0
                self._nvidia_client.timeout = timeout_override

            stream = self._nvidia_client.chat.completions.create(
                model=self.NVIDIA_MODEL,
                messages=messages,
                max_tokens=max(mt, 1024),
                temperature=self._temperature,
                top_p=1.0,
                stream=True,
                **({"extra_body": extra} if extra else {}),
            )
            chunks = []
            for chunk in stream:
                delta = chunk.choices[0].delta.content or "" if chunk.choices else ""
                chunks.append(delta)
            text = "".join(chunks)
            # Remove <think>…</think> reasoning traces
            text = re.sub(r"<think>[\s\S]*?</think>", "", text, flags=re.DOTALL).strip()
            if text:
                mode = "thinking" if self._nvidia_thinking else "fast"
                logger.debug(f"Response from NVIDIA NIM ({mode})")
                self.last_provider = "nvidia"
                return text
        except Exception as e:
            logger.warning(f"NVIDIA NIM: {e}")
        return ""

    def _try_openrouter(self, messages: List[Dict], mt: int) -> str:
        if not self._openrouter_client:
            return ""
        for model in self._fast_models:
            try:
                resp = self._openrouter_client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=mt,
                    temperature=self._temperature,
                    extra_headers={"HTTP-Referer": "loki-desktop-assistant", "X-Title": "Loki"},
                )
                text = resp.choices[0].message.content or ""
                if text.strip():
                    logger.debug(f"Response from OpenRouter ({model})")
                    self.last_provider = f"openrouter:{model}"
                    return text
            except Exception as e:
                logger.warning(f"OpenRouter {model}: {e}")
        return ""

    def _try_kimi(self, messages: List[Dict], mt: int) -> str:
        if not self._kimi_client:
            return ""
        try:
            resp = self._kimi_client.chat.completions.create(
                model=self._kimi_model,
                messages=messages,
                max_tokens=mt,
                temperature=self._temperature,
            )
            text = resp.choices[0].message.content or ""
            if text.strip():
                logger.debug("Response from Kimi Moonshot")
                self.last_provider = "kimi"
                return text
        except Exception as e:
            logger.warning(f"Kimi Moonshot: {e}")
        return ""

    def _try_ollama(self, messages: List[Dict], mt: int) -> str:
        local = self._call_ollama(messages, mt)
        if local:
            self.last_provider = "ollama"
            return local
        return ""

    def _call_llm(self, messages: List[Dict], max_tokens: int = None) -> str:
        mt = max_tokens or self._max_tokens
        calls = {
            "ollama": self._try_ollama,
            "nvidia": self._try_nvidia,
            "openrouter": self._try_openrouter,
            "kimi": self._try_kimi,
        }

        # Default priority. When prefer_local, the local model stays pinned first
        # (you asked to keep qwen primary); the bandit only reorders the cloud
        # fallbacks. Otherwise the bandit ranks the whole set.
        cloud = ["nvidia", "openrouter", "kimi"]
        if self._bandit:
            cloud = self._bandit.rank(cloud)

        order = (["ollama"] + cloud) if self._prefer_local else (cloud + ["ollama"])

        for name in order:
            text = calls[name](messages, mt)
            if text:
                return text

        self.last_provider = "none"
        return ""

    # ─── Public ask interface ─────────────────────────────────────────────────

    # well-known sites → open directly in the browser
    _SITES = {
        "youtube": "youtube.com", "gmail": "mail.google.com", "google": "google.com",
        "github": "github.com", "reddit": "reddit.com", "twitter": "twitter.com",
        "x": "x.com", "facebook": "facebook.com", "instagram": "instagram.com",
        "whatsapp": "web.whatsapp.com", "netflix": "netflix.com", "amazon": "amazon.com",
        "wikipedia": "wikipedia.org", "linkedin": "linkedin.com", "chatgpt": "chat.openai.com",
        "maps": "maps.google.com", "drive": "drive.google.com",
    }
    # filler words stripped when extracting a search topic
    _FILLER = {"a", "an", "the", "tab", "with", "something", "some", "stuff", "for", "about",
               "on", "in", "there", "please", "pls", "can", "you", "u", "and", "open", "go",
               "to", "of", "me", "show", "find", "search", "look", "up", "play", "watch", "new"}

    @classmethod
    def _fast_intent(cls, text: str) -> Optional[str]:
        """Deterministic fast-path for common device/web commands — bypasses the LLM
        so PC control works 100% reliably even with a weak local model. Returns a
        JSON intent string (which parse_intent then handles) or None to fall through."""
        t = text.lower().strip().rstrip("?.!")
        m = None

        # ── MULTI-STEP automation → hand to the agent ───────────────────────
        # genuine sequences: "X then Y", or "open … and <do something> …"
        _act2 = r"(?:type|write|save|create|make|generate|fill|enter|draft|compose|then)"
        # (youtube "open … and search" is one action — handled by the youtube block below)
        if "youtube" not in t and (
                " then " in t
                or re.search(rf"\b(?:open|launch|start)\b.{{0,50}}\band\b.{{0,30}}\b{_act2}\b", t)
                or re.search(rf"\b{_act2}\b.{{0,40}}\b(?:and|then)\b.{{0,25}}\b(?:save|press|enter|it|that)\b", t)):
            return json.dumps({"intent": "agent_run", "params": {"goal": text.strip()},
                               "message": "On it — running that as a sequence."})

        def topic_after(keyword: str) -> str:
            """Pull the meaningful search topic out of a messy command."""
            tail = t.split(keyword, 1)[-1]
            words = [w for w in re.findall(r"[a-z0-9']+", tail) if w not in cls._FILLER]
            return " ".join(words).strip()

        # ── YOUTUBE — search/play a topic, or just open it ──────────────────
        if "youtube" in t:
            topic = topic_after("youtube")
            # also catch "pokemon ... youtube" (topic before the word)
            if not topic:
                head = t.split("youtube", 1)[0]
                topic = " ".join(w for w in re.findall(r"[a-z0-9']+", head) if w not in cls._FILLER)
            if topic:
                return json.dumps({"intent": "browser_search", "params": {"query": topic, "engine": "youtube"},
                                   "message": f"Searching YouTube for {topic}."})
            return json.dumps({"intent": "browser_open", "params": {"url": "youtube.com"}, "message": "Opening YouTube."})

        # ── search the web (explicit) — but NOT "open google chrome" etc. ────
        m = re.search(r"\b(?:google|search(?:\s+the\s+web)?|look up)\s+(?:for\s+)?(.+)", t)
        if m and "youtube" not in t and not re.match(r"^\s*(?:open|launch|go to|visit|start)\b", t):
            return json.dumps({"intent": "browser_search", "params": {"query": m.group(1).strip()}, "message": "Searching."})

        # ── open a known site or a URL ──────────────────────────────────────
        m = re.search(r"\b(?:open|go to|visit|launch)\s+(?:the\s+|my\s+|app\s+|website\s+)?(.+)", t)
        if m:
            tgt = m.group(1).strip()
            # clip at the first conjunction — an app/site name is short, not a sentence
            # ("open notepad and write a poem" → name = "notepad", the rest is multi-step)
            tgt = re.split(r"\b(?:and|then|to|with|for|so that)\b|,", tgt, 1)[0].strip()
            # cap to 4 words max (covers "visual studio code", "microsoft edge")
            tgt = " ".join(tgt.split()[:4])
            if not tgt:
                return None
            # explicit url
            if re.search(r"\.(com|org|net|io|ai|dev|co|gov|edu|uk)\b", tgt) or tgt.startswith("http"):
                return json.dumps({"intent": "browser_open", "params": {"url": tgt}, "message": "Opening it."})
            # known website word — only when it's a SINGLE word ("open reddit"),
            # so "open google chrome" still opens the Chrome app, not google.com
            words = tgt.split()
            if len(words) == 1 and words[0] in cls._SITES:
                return json.dumps({"intent": "browser_open", "params": {"url": cls._SITES[words[0]]}, "message": f"Opening {words[0]}."})
            # otherwise it's an app
            return json.dumps({"intent": "app_open", "params": {"name": tgt}, "message": f"Opening {tgt}."})

        # close / quit app
        m = re.search(r"\b(?:close|quit|exit|kill|stop)\s+(?:the\s+|my\s+|app\s+)?(.+)", t)
        if m and "process" not in t:
            return json.dumps({"intent": "app_close", "params": {"name": m.group(1).strip()}, "message": "Closing it."})

        # volume set
        m = re.search(r"\b(?:set\s+)?volume\s+(?:to\s+)?(\d{1,3})", t) or re.search(r"\b(\d{1,3})\s*(?:percent\s+)?volume", t)
        if m:
            return json.dumps({"intent": "volume_set", "params": {"percent": int(m.group(1))}, "message": f"Volume to {m.group(1)}%."})
        # volume get
        if re.search(r"\b(?:what|check|current|how loud).*volume|^volume$|my volume", t):
            return json.dumps({"intent": "volume_get", "params": {}, "message": "Checking volume."})
        # mute
        if re.search(r"\b(?:mute|silence)\b", t):
            return json.dumps({"intent": "volume_set", "params": {"percent": 0}, "message": "Muting."})

        # brightness set
        m = re.search(r"\b(?:set\s+)?brightness\s+(?:to\s+)?(\d{1,3})", t) or re.search(r"\b(?:dim|brighten).*?(\d{1,3})", t)
        if m:
            return json.dumps({"intent": "brightness_set", "params": {"percent": int(m.group(1))}, "message": f"Brightness to {m.group(1)}%."})
        if re.search(r"\b(?:what|check|current).*brightness|^brightness$|my brightness", t):
            return json.dumps({"intent": "brightness_get", "params": {}, "message": "Checking brightness."})

        # system stats
        if re.search(r"\b(?:cpu|ram|memory|system stat|system health|how.*(?:pc|computer|system|machine).*(?:doing|running)|resource usage|disk space)\b", t):
            return json.dumps({"intent": "system_monitor", "params": {}, "message": "Reading system stats."})

        # processes
        if re.search(r"\b(?:list|show|what).*(?:process|running app|task)", t):
            return json.dumps({"intent": "process_list", "params": {}, "message": "Listing processes."})

        # ── GOOGLE — calendar + gmail ───────────────────────────────────────
        if re.search(r"\b(?:my )?(?:calendar|schedule|agenda)\b|what.?s on (?:today|my day)|what do i have (?:today|on)", t):
            return json.dumps({"intent": "calendar_today", "params": {"days": 1}, "message": "Checking your calendar."})
        if re.search(r"\bnext (?:meeting|event|appointment)\b|when.?s my next", t):
            return json.dumps({"intent": "calendar_next", "params": {}, "message": "Checking."})
        if re.search(r"\b(?:any )?(?:new |unread )?(?:e?mail|inbox|messages)\b", t) and "search" not in t:
            return json.dumps({"intent": "email_unread", "params": {}, "message": "Checking your inbox."})

        # ── SPOTIFY — playback control ──────────────────────────────────────
        m = re.match(r"^(?:hey )?(?:loki[,\s]+)?(?:play|put on) (.+?)(?: on spotify)?$", t)
        if m and "youtube" not in t:
            return json.dumps({"intent": "spotify_play", "params": {"query": m.group(1).strip()}, "message": "Playing."})
        if re.search(r"what.?s (?:playing|this song)|current(?:ly)? (?:playing|song|track)|now playing", t):
            return json.dumps({"intent": "spotify_now", "params": {}, "message": "Checking."})
        if re.fullmatch(r"(?:hey loki[,\s]+)?(?:pause|pause (?:the )?(?:music|song|spotify))\.?", t):
            return json.dumps({"intent": "spotify_pause", "params": {}, "message": "Paused."})
        if re.fullmatch(r"(?:hey loki[,\s]+)?(?:resume|play|unpause)\.?", t):
            return json.dumps({"intent": "spotify_play", "params": {}, "message": "Playing."})
        if re.search(r"\b(?:skip|next (?:song|track))\b", t):
            return json.dumps({"intent": "spotify_next", "params": {}, "message": "Skipped."})
        if re.search(r"\b(?:previous|last) (?:song|track)\b|\bgo back a (?:song|track)\b", t):
            return json.dumps({"intent": "spotify_previous", "params": {}, "message": "Back a track."})

        # ── SECOND BRAIN — personal memory ──────────────────────────────────
        m = re.match(r"^(?:hey )?(?:loki[,\s]+)?remember (?:that |this[:,]? )?(.+)$", t)
        if m:
            return json.dumps({"intent": "remember", "params": {"text": m.group(1).strip()}, "message": "Noted."})
        m = re.match(r"^(?:what (?:did i|do you) (?:say|know|remember)|what.?s|recall|do you remember)\b.*?\babout (.+?)\??$", t)
        if m:
            return json.dumps({"intent": "recall", "params": {"query": m.group(1).strip()}, "message": "Let me think."})
        if re.fullmatch(r"(?:list|show) (?:my )?notes\.?", t):
            return json.dumps({"intent": "notes_list", "params": {}, "message": "Your notes."})

        # ── VISION — look at the screen and answer ─────────────────────────
        # "what's on my screen", "what's this error", "look at my screen", "what am I looking at"
        if (re.search(r"\b(?:what'?s|what is|whats|describe|explain|summari[sz]e|read|look at|check)\b.{0,30}\b(?:screen|display|this|page|error|here|window)\b", t)
                or re.search(r"\bwhat am i (?:looking at|seeing|on)\b", t)
                or t in ("what's this", "whats this", "look at this", "what is this")):
            return json.dumps({"intent": "screen_ask", "params": {"question": text.strip()},
                               "message": "Let me take a look."})
        # type text  →  type "hello"  /  type hello world
        m = re.search(r'\btype\s+(?:out\s+)?["\']?(.+?)["\']?$', t)
        if m:
            return json.dumps({"intent": "computer_type", "params": {"text": m.group(1)}, "message": "Typing."})
        # press a key / hotkey  →  press enter / press ctrl+s
        m = re.search(r"\bpress\s+(?:the\s+)?(.+)", t)
        if m:
            return json.dumps({"intent": "computer_press", "params": {"key": m.group(1).replace(" plus ", "+").strip()}, "message": "Pressing."})
        # scroll
        if re.search(r"\bscroll\s+up\b", t):
            return json.dumps({"intent": "computer_scroll", "params": {"amount": 500}, "message": "Scrolling up."})
        if re.search(r"\bscroll\s+down\b", t) or t == "scroll":
            return json.dumps({"intent": "computer_scroll", "params": {"amount": -500}, "message": "Scrolling down."})
        # click on text  →  click on Submit / click the Save button
        m = re.search(r"\bclick\s+(?:on\s+|the\s+)?(.+?)(?:\s+button)?$", t)
        if m and m.group(1) not in ("here", "it"):
            return json.dumps({"intent": "computer_click_text", "params": {"target": m.group(1).strip()}, "message": "Clicking."})
        # desktop actions
        for phrase, act in [
            ("show desktop", "show desktop"), ("minimize", "minimize"), ("maximize", "maximize"),
            ("switch window", "switch window"), ("close window", "close window"),
            ("lock the screen", "lock"), ("lock screen", "lock"), ("take a screenshot", "screenshot"),
            ("screenshot", "screenshot"), ("select all", "select all"), ("new tab", "new tab"),
            ("close tab", "close tab"), ("paste", "paste"), ("copy that", "copy"), ("save this", "save"),
        ]:
            if phrase in t:
                return json.dumps({"intent": "computer_action", "params": {"action": act}, "message": f"{act.title()}."})

        return None

    def ask_vision(self, question: str, image_b64: str) -> str:
        """Answer a question about an image (a screenshot) using a vision model.
        Returns '' if no vision-capable provider is reachable."""
        if not self._openrouter_client:
            return ""
        content = [
            {"type": "text", "text": question},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}},
        ]
        messages = [
            {"role": "system", "content": self._build_system_prompt()},
            {"role": "user", "content": content},
        ]
        for model in self._vision_models:
            try:
                resp = self._openrouter_client.chat.completions.create(
                    model=model, messages=messages, max_tokens=500, temperature=0.4,
                    extra_headers={"HTTP-Referer": "loki-desktop-assistant", "X-Title": "Loki"},
                )
                text = (resp.choices[0].message.content or "").strip()
                if text:
                    logger.debug(f"Vision answer from {model}")
                    return text
            except Exception as e:
                logger.warning(f"Vision model {model}: {e}")
        return ""

    def ask(self, user_message: str, is_wakeword: bool = False) -> Generator[str, None, None]:
        if is_wakeword:
            yield random.choice(WAKEWORD_RESPONSES)
            return

        logger.debug(f"User message: {user_message[:100]}")

        # Deterministic fast-path for common PC commands — reliable regardless of model
        fast = self._fast_intent(user_message)
        if fast:
            logger.debug("Fast-path intent matched (bypassed LLM)")
            self.last_provider = "fast_path"
            yield fast
            self._store_turn(user_message, fast)
            return

        # Gather all context layers in parallel (fast: KG is in-memory, RAG hits ChromaDB)
        kg_context = self._get_kg_context(user_message)
        rag_context = self._get_rag_context(user_message)

        ctx_bits = []
        if kg_context:
            ctx_bits.append(f"KG +{len(kg_context)}c")
        if rag_context:
            ctx_bits.append(f"RAG +{len(rag_context)}c")
        if ctx_bits:
            logger.debug(f"context: {', '.join(ctx_bits)}")

        messages = self._build_messages(user_message, kg_context, rag_context)
        _start = time.time()
        response_text = self._call_llm(messages)
        logger.debug(f"LLM responded in {time.time() - _start:.1f}s")

        if not response_text.strip():
            response_text = "All pathways to knowledge are severed. Check your API keys and try again."
            logger.error("all LLM providers failed — check API keys / network")

        yield response_text
        self._store_turn(user_message, response_text)

    # ─── Memory maintenance ───────────────────────────────────────────────────

    def _store_turn(self, user_msg: str, assistant_msg: str) -> None:
        # Append + persist immediately (fast — just a JSON write)
        with self._history_lock:
            self._conversation_history.append({"role": "user", "content": user_msg})
            self._conversation_history.append({"role": "assistant", "content": assistant_msg})
            self._exchange_count += 1
            need_compress = len(self._conversation_history) > COMPRESSION_THRESHOLD
            need_facts = self._exchange_count % FACT_EXTRACT_EVERY == 0
        self._save_history()

        # Heavy LLM-based maintenance (compression, fact extraction) runs on a
        # background thread so it NEVER delays the spoken response. Previously these
        # blocking calls ran inline, adding 5-60s latency every few turns.
        if (need_compress or need_facts) and not self._maint_running:
            self._maint_running = True
            threading.Thread(
                target=self._run_maintenance,
                args=(user_msg, assistant_msg, need_compress, need_facts),
                daemon=True,
                name="loki-memory-maint",
            ).start()

    def _run_maintenance(self, user_msg: str, assistant_msg: str,
                         do_compress: bool, do_facts: bool) -> None:
        try:
            if do_compress:
                self._compress_old_turns()
            if do_facts:
                self._extract_facts(user_msg, assistant_msg)
        except Exception as e:
            logger.warning(f"Memory maintenance error: {e}")
        finally:
            self._maint_running = False

    def _compress_old_turns(self) -> None:
        if not self._brain_memory:
            with self._history_lock:
                self._conversation_history = self._conversation_history[-self._max_turns * 2:]
            return

        # Snapshot the batch to compress (under lock), run LLM (no lock), then trim (lock)
        with self._history_lock:
            to_compress = list(self._conversation_history[:COMPRESSION_BATCH])
        convo_text = "\n".join(
            f"{m['role'].upper()}: {m['content'][:300]}" for m in to_compress
        )
        summary_prompt = [
            {"role": "system", "content": "You summarize conversations concisely."},
            {"role": "user", "content": (
                f"Summarize these {len(to_compress)} messages in 2-3 sentences, "
                f"capturing key decisions, facts learned, and tasks discussed:\n\n{convo_text}"
            )},
        ]
        summary = self._call_llm(summary_prompt, max_tokens=150)

        with self._history_lock:
            self._conversation_history = self._conversation_history[COMPRESSION_BATCH:]
        if summary:
            self._brain_memory.add_session_summary(summary)
            logger.info(f"Compressed {len(to_compress)} messages → session summary")
        self._save_history()

    def _extract_facts(self, user_msg: str, assistant_msg: str) -> None:
        if not self._brain_memory:
            return
        prompt = [
            {"role": "system", "content": "You extract memorable facts from conversations."},
            {"role": "user", "content": (
                f"From this exchange, extract 0-3 facts worth remembering long-term. "
                f"If nothing notable, reply 'NONE'.\n\n"
                f"USER: {user_msg[:500]}\nASSISTANT: {assistant_msg[:500]}\n\n"
                f"Reply with one fact per line, or 'NONE'."
            )},
        ]
        result = self._call_llm(prompt, max_tokens=100)
        if result and result.strip().upper() != "NONE":
            facts = [line.strip("- •").strip() for line in result.splitlines() if line.strip()]
            self._brain_memory.add_key_facts(facts)
            logger.info(f"Extracted {len(facts)} facts from exchange")

    # ─── Intent parsing ───────────────────────────────────────────────────────

    def parse_intent(self, response_text: str) -> Optional[Dict[str, Any]]:
        text = response_text.strip()

        # Unwrap fenced code blocks if present
        if "```json" in text:
            start = text.find("```json") + 7
            end = text.find("```", start)
            text = text[start:end].strip() if end != -1 else text[start:].strip()
        elif "```" in text:
            start = text.find("```") + 3
            end = text.find("```", start)
            text = text[start:end].strip() if end != -1 else text[start:].strip()

        # Fast path: whole thing is a JSON object
        candidate = text if (text.startswith("{") and text.endswith("}")) else None

        # Otherwise extract the first balanced {...} block (handles prose around JSON)
        if candidate is None:
            depth = 0
            obj_start = -1
            for idx, ch in enumerate(text):
                if ch == "{":
                    if depth == 0:
                        obj_start = idx
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0 and obj_start != -1:
                        candidate = text[obj_start:idx + 1]
                        break

        if not candidate:
            return None
        try:
            intent = json.loads(candidate)
            if not isinstance(intent, dict) or "intent" not in intent:
                return None
            return intent
        except json.JSONDecodeError:
            return None

    # ─── Utilities ────────────────────────────────────────────────────────────

    def get_dismissal_message(self) -> str:
        return random.choice(DISMISSAL_MESSAGES)

    def clear_conversation(self) -> None:
        with self._history_lock:
            self._conversation_history.clear()
        self._save_history()

    def get_user_name(self) -> str:
        if self._brain_memory:
            return self._brain_memory.user_name
        return "User"

    def set_user_name(self, name: str) -> None:
        if self._brain_memory:
            self._brain_memory.user_name = name

    def get_conversation_summary(self) -> str:
        count = len(self._conversation_history) // 2
        return f"{count} exchanges in memory"
