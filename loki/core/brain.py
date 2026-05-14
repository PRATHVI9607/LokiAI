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
from typing import Dict, Any, List, Optional, Generator
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

logger = logging.getLogger(__name__)

# ─── Intent catalog ───────────────────────────────────────────────────────────

INTENT_CATALOG = """

CAPABILITIES — respond with JSON for any PC action:
{"intent": "<intent>", "params": {}, "message": "brief acknowledgment"}

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

INTENTS (misc):
- undo: params={}
- chat: params={}  (no action, pure conversation)

SECURITY RULES:
- For destructive ops (file_delete, folder_delete, process_kill), always include a confirmation request in your message.
- Never reveal vault contents in the message field.
- Validate that file paths seem reasonable before confirming.

For pure conversation (no action needed), respond naturally without JSON."""

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
    LLM priority: Kimi K2 → OpenRouter → Ollama.
    Context layers: personality + brain memory + KG entities + RAG chunks + history.
    """

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

        # ─── Provider 1: Kimi K2 (Moonshot API) ──────────────────────────────
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
                logger.info(f"Kimi K2 configured: {self._kimi_model}")
            except Exception as e:
                logger.warning(f"Kimi K2 init failed: {e}")
        else:
            logger.info("KIMI_API_KEY not set — Kimi K2 disabled")

        # ─── Provider 2: OpenRouter ────────────────────────────────────────────
        self._openrouter_client: Optional[Any] = None
        or_key = os.getenv("OPENROUTER_API_KEY", "")
        if or_key and or_key not in ("your_openrouter_api_key_here", ""):
            try:
                self._openrouter_client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=or_key,
                    timeout=60.0,
                )
                logger.info("OpenRouter configured")
            except Exception as e:
                logger.warning(f"OpenRouter init failed: {e}")
        else:
            logger.warning("OPENROUTER_API_KEY not set")

        self._fallback_models = [
            config.get("fallback_model", "mistralai/mistral-7b-instruct:free"),
            config.get("second_fallback_model", "google/gemma-2-9b-it:free"),
        ]

        # ─── Provider 3: Ollama (local) ────────────────────────────────────────
        self._ollama_infer_client: Optional[Any] = None
        self._ollama_model = config.get("ollama_model", "phi3:mini")
        self._ollama_available = False
        try:
            probe = OpenAI(
                base_url="http://localhost:11434/v1",
                api_key="ollama",
                timeout=3.0,
                max_retries=0,
            )
            probe.models.list()
            self._ollama_infer_client = OpenAI(
                base_url="http://localhost:11434/v1",
                api_key="ollama",
                timeout=120.0,
                max_retries=0,
            )
            self._ollama_available = True
            logger.info(f"Ollama connected: {self._ollama_model}")
        except Exception:
            logger.info("Ollama not running — local inference disabled")

        self._conversation_file = self._memory_dir / "conversation.json"
        self._conversation_history: List[Dict[str, str]] = []
        self._exchange_count = 0

        self._load_history()
        self._log_provider_status()

    def _log_provider_status(self) -> None:
        primary = "Kimi K2" if self._kimi_client else ("OpenRouter" if self._openrouter_client else "Ollama")
        logger.info(f"Brain active — primary provider: {primary}")

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
        try:
            with open(self._conversation_file, "w", encoding="utf-8") as f:
                json.dump(
                    self._conversation_history[-(self._max_turns * 2):],
                    f, indent=2, ensure_ascii=False,
                )
        except Exception as e:
            logger.error(f"Failed to save conversation: {e}")

    # ─── Context assembly ─────────────────────────────────────────────────────

    def _build_system_prompt(self) -> str:
        if self._brain_memory:
            personality_prompt = self._brain_memory.get_personality_prompt()
        else:
            from loki.core.brain_memory import PERSONALITY_PROMPTS
            personality_prompt = PERSONALITY_PROMPTS["loki"]

        system = personality_prompt + INTENT_CATALOG

        if self._brain_memory:
            memory_ctx = self._brain_memory.get_memory_context()
            if memory_ctx:
                system += f"\n\n## What you know about this user:\n{memory_ctx}"

        return system

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

        messages.extend(self._conversation_history[-(self._max_turns * 2):])
        messages.append({"role": "user", "content": user_message})
        return messages

    # ─── Inference ────────────────────────────────────────────────────────────

    def _call_llm(self, messages: List[Dict], max_tokens: int = None) -> str:
        mt = max_tokens or self._max_tokens

        # 1. Kimi K2
        if self._kimi_client:
            try:
                resp = self._kimi_client.chat.completions.create(
                    model=self._kimi_model,
                    messages=messages,
                    max_tokens=mt,
                    temperature=self._temperature,
                )
                text = resp.choices[0].message.content or ""
                if text.strip():
                    logger.debug("Response from Kimi K2")
                    return text
            except Exception as e:
                logger.warning(f"Kimi K2 error: {e} — trying OpenRouter")

        # 2. OpenRouter
        if self._openrouter_client:
            for model in self._fallback_models:
                try:
                    resp = self._openrouter_client.chat.completions.create(
                        model=model,
                        messages=messages,
                        max_tokens=mt,
                        temperature=self._temperature,
                        extra_headers={
                            "HTTP-Referer": "loki-desktop-assistant",
                            "X-Title": "Loki",
                        },
                    )
                    text = resp.choices[0].message.content or ""
                    if text.strip():
                        logger.debug(f"Response from OpenRouter ({model})")
                        return text
                except Exception as e:
                    logger.warning(f"OpenRouter error ({model}): {e}")

        # 3. Ollama (local)
        if self._ollama_available and self._ollama_infer_client:
            try:
                resp = self._ollama_infer_client.chat.completions.create(
                    model=self._ollama_model,
                    messages=messages,
                    max_tokens=mt,
                    temperature=self._temperature,
                )
                text = resp.choices[0].message.content or ""
                if text.strip():
                    logger.debug(f"Response from Ollama ({self._ollama_model})")
                    return text
            except Exception as e:
                logger.warning(f"Ollama error: {e}")

        return ""

    # ─── Public ask interface ─────────────────────────────────────────────────

    def ask(self, user_message: str, is_wakeword: bool = False) -> Generator[str, None, None]:
        if is_wakeword:
            yield random.choice(WAKEWORD_RESPONSES)
            return

        logger.info(f"User: {user_message[:100]}")

        # Gather all context layers in parallel (fast: KG is in-memory, RAG hits ChromaDB)
        kg_context = self._get_kg_context(user_message)
        rag_context = self._get_rag_context(user_message)

        if kg_context:
            logger.info(f"KG: injecting {len(kg_context)} chars of entity context")
        if rag_context:
            logger.info(f"RAG: injecting {len(rag_context)} chars of file context")

        messages = self._build_messages(user_message, kg_context, rag_context)
        response_text = self._call_llm(messages)

        if not response_text.strip():
            response_text = "All pathways to knowledge are severed. Check your API keys and try again."
            logger.error("All LLM backends failed")

        logger.info(f"Loki: {response_text[:80]}")
        yield response_text
        self._store_turn(user_message, response_text)

    # ─── Memory maintenance ───────────────────────────────────────────────────

    def _store_turn(self, user_msg: str, assistant_msg: str) -> None:
        self._conversation_history.append({"role": "user", "content": user_msg})
        self._conversation_history.append({"role": "assistant", "content": assistant_msg})
        self._exchange_count += 1
        self._save_history()

        if len(self._conversation_history) > COMPRESSION_THRESHOLD:
            self._compress_old_turns()

        if self._exchange_count % FACT_EXTRACT_EVERY == 0:
            self._extract_facts(user_msg, assistant_msg)

    def _compress_old_turns(self) -> None:
        if not self._brain_memory:
            self._conversation_history = self._conversation_history[-self._max_turns * 2:]
            return

        to_compress = self._conversation_history[:COMPRESSION_BATCH]
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
        try:
            summary = self._call_llm(summary_prompt, max_tokens=150)
        except Exception as e:
            logger.warning(f"Compression failed: {e}")
            return

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
        if "```json" in text:
            start = text.find("```json") + 7
            end = text.find("```", start)
            text = text[start:end].strip()
        elif "```" in text:
            start = text.find("```") + 3
            end = text.find("```", start)
            text = text[start:end].strip()

        if not (text.startswith("{") and text.endswith("}")):
            return None
        try:
            intent = json.loads(text)
            if "intent" not in intent:
                return None
            return intent
        except json.JSONDecodeError:
            return None

    # ─── Utilities ────────────────────────────────────────────────────────────

    def get_dismissal_message(self) -> str:
        return random.choice(DISMISSAL_MESSAGES)

    def clear_conversation(self) -> None:
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
