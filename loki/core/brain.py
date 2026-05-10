"""
Loki's brain — LLM integration with KORTEX-style context engineering.

Context priority (from KORTEX PRD):
  1. System prompt (personality + intent catalog)
  2. Brain memory (key facts, decisions, session summaries)
  3. RAG context (relevant chunks from uploaded files)
  4. Recent chat history (last N turns)
  5. User message

Auto-compression: when history exceeds threshold, oldest turns are summarized
by Ollama and stored in brain_memory as session summaries.

Fact extraction: every 5 exchanges, Ollama scans the last exchange for
memorable facts and appends them to brain_memory.key_facts.
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

# ─── Personality-agnostic intent catalog (appended to any personality prompt) ─

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

# Compress oldest turns when history exceeds this many messages
COMPRESSION_THRESHOLD = 40  # 20 exchanges
COMPRESSION_BATCH = 20       # compress this many at once
FACT_EXTRACT_EVERY = 5       # extract facts every N exchanges


class LokiBrain:
    """
    LLM integration with KORTEX-style context engineering, memory,
    auto-compression, fact extraction, and personality modes.
    """

    def __init__(
        self,
        config: dict,
        memory_dir: Path,
        brain_memory=None,   # BrainMemory instance (optional)
        rag_engine=None,     # RagEngine instance (optional)
    ):
        if OpenAI is None:
            raise ImportError("openai package required: pip install openai")

        self._config = config
        self._memory_dir = Path(memory_dir)
        self._brain_memory = brain_memory
        self._rag_engine = rag_engine

        # ─── Ollama ───────────────────────────────────────────────────────────
        self._ollama_probe_client: Optional[Any] = None
        self._ollama_infer_client: Optional[Any] = None
        self._ollama_model = config.get("ollama_model", "phi3:mini")
        self._ollama_available = False

        try:
            self._ollama_probe_client = OpenAI(
                base_url="http://localhost:11434/v1",
                api_key="ollama",
                timeout=3.0,
                max_retries=0,
            )
            self._ollama_probe_client.models.list()
            self._ollama_infer_client = OpenAI(
                base_url="http://localhost:11434/v1",
                api_key="ollama",
                timeout=120.0,
                max_retries=0,
            )
            self._ollama_available = True
            logger.info(f"Ollama connected: {self._ollama_model}")
        except Exception:
            logger.info("Ollama not running — using OpenRouter.")

        # ─── OpenRouter ───────────────────────────────────────────────────────
        self._openrouter_client: Optional[Any] = None
        api_key = os.getenv("OPENROUTER_API_KEY", "")
        if api_key and api_key != "your_openrouter_api_key_here":
            self._openrouter_client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
            )
            logger.info("OpenRouter configured")
        else:
            logger.warning("OPENROUTER_API_KEY not set")

        self._fallback_models = [
            config.get("fallback_model", "mistralai/mistral-7b-instruct:free"),
            config.get("second_fallback_model", "google/gemma-2-9b-it:free"),
        ]

        self._max_tokens = config.get("max_tokens", 400)
        self._temperature = config.get("temperature", 0.75)
        self._max_turns = config.get("max_turns", 20)

        self._conversation_file = self._memory_dir / "conversation.json"
        self._conversation_history: List[Dict[str, str]] = []
        self._exchange_count = 0  # tracks exchanges since last fact extraction

        self._load_history()
        logger.info("Loki brain initialized")

    # ─── Memory loading ───────────────────────────────────────────────────────

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
                json.dump(self._conversation_history[-self._max_turns * 2:], f,
                          indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save conversation: {e}")

    # ─── Context assembly (KORTEX priority model) ─────────────────────────────

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

    def _build_messages(self, user_message: str, rag_context: str = "") -> List[Dict[str, str]]:
        """
        Assemble context in KORTEX priority order:
        1. System prompt + brain memory
        2. RAG context (file knowledge) — as separate system message
        3. Recent chat history
        4. User message
        """
        messages: List[Dict[str, str]] = [
            {"role": "system", "content": self._build_system_prompt()}
        ]

        if rag_context:
            messages.append({"role": "system", "content": rag_context})

        # Use last max_turns exchanges (each exchange = 2 messages)
        messages.extend(self._conversation_history[-(self._max_turns * 2):])
        messages.append({"role": "user", "content": user_message})
        return messages

    def _get_rag_context(self, user_message: str) -> str:
        if not self._rag_engine or not self._rag_engine.is_available:
            return ""
        results = self._rag_engine.query(user_message, top_k=5)
        if not results:
            return ""
        return self._rag_engine.format_context(results)

    # ─── Inference ────────────────────────────────────────────────────────────

    def _call_llm(self, messages: List[Dict], max_tokens: int = None) -> str:
        mt = max_tokens or self._max_tokens

        if self._ollama_available and self._ollama_infer_client:
            try:
                response = self._ollama_infer_client.chat.completions.create(
                    model=self._ollama_model,
                    messages=messages,
                    max_tokens=mt,
                    temperature=self._temperature,
                )
                text = response.choices[0].message.content or ""
                if text.strip():
                    return text
            except Exception as e:
                logger.warning(f"Ollama error: {e}")

        if self._openrouter_client:
            for model in self._fallback_models:
                try:
                    response = self._openrouter_client.chat.completions.create(
                        model=model,
                        messages=messages,
                        max_tokens=mt,
                        temperature=self._temperature,
                        extra_headers={
                            "HTTP-Referer": "loki-desktop-assistant",
                            "X-Title": "Loki",
                        },
                    )
                    text = response.choices[0].message.content or ""
                    if text.strip():
                        return text
                except Exception as e:
                    logger.error(f"OpenRouter error ({model}): {e}")

        return ""

    # ─── Public ask interface ─────────────────────────────────────────────────

    def ask(self, user_message: str, is_wakeword: bool = False) -> Generator[str, None, None]:
        if is_wakeword:
            yield random.choice(WAKEWORD_RESPONSES)
            return

        logger.info(f"User: {user_message[:100]}")

        # Priority 3: RAG context from uploaded files
        rag_context = self._get_rag_context(user_message)
        if rag_context:
            logger.info(f"RAG: injecting {len(rag_context)} chars of file context")

        messages = self._build_messages(user_message, rag_context)
        response_text = self._call_llm(messages)

        if not response_text.strip():
            response_text = "Apologies. My connection to the realms of knowledge is severed. Try again."
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

        # Auto-compress when history gets too long
        if len(self._conversation_history) > COMPRESSION_THRESHOLD:
            self._compress_old_turns()

        # Periodically extract facts
        if self._exchange_count % FACT_EXTRACT_EVERY == 0:
            self._extract_facts(user_msg, assistant_msg)

    def _compress_old_turns(self) -> None:
        """
        Summarize the oldest COMPRESSION_BATCH messages via Ollama,
        store summary in brain_memory, drop those messages from history.
        History is only mutated after a successful LLM call.
        """
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
            logger.warning(f"Compression LLM call failed: {e} — history unchanged")
            return

        # Only mutate history after LLM succeeds
        self._conversation_history = self._conversation_history[COMPRESSION_BATCH:]
        if summary:
            self._brain_memory.add_session_summary(summary)
            logger.info(f"Compressed {len(to_compress)} messages → session summary")
        self._save_history()

    def _extract_facts(self, user_msg: str, assistant_msg: str) -> None:
        """
        Ask the LLM to extract memorable facts from the last exchange.
        Facts are stored in brain_memory.key_facts.
        """
        if not self._brain_memory:
            return

        prompt = [
            {"role": "system", "content": "You extract memorable facts from conversations."},
            {"role": "user", "content": (
                f"From this exchange, extract 0-3 facts worth remembering long-term about the user, "
                f"their system, preferences, or project. If nothing notable, reply 'NONE'.\n\n"
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
