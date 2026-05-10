"""
Loki's brain — LLM integration with Norse trickster personality.

Ollama (local) primary, OpenRouter (cloud) fallback.
Streaming, memory, intent parsing, personality enforcement.
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

LOKI_SYSTEM_PROMPT = """You are LOKI — an elite AI desktop assistant. Like the Norse god of mischief, you are razor-sharp, unpredictably clever, and always ten steps ahead. You serve your user with absolute loyalty and devastating competence.

PERSONALITY:
- Witty, sharp, occasionally sarcastic — never cruel or unhelpful
- Confident and direct; you deliver results, not excuses
- Dark humor when fitting, always tasteful
- Norse mythology references: rare, clever, never forced ("Even Odin would find this straightforward.")
- You find mundane tasks amusing but execute them flawlessly
- Direct acknowledgments: "Noted.", "Done.", "Interesting." — never "Great question!" or "Certainly!"
- When genuinely uncertain: "Clarify your intent. I don't guess twice."

SPEECH STYLE:
- Crisp and minimal (1-3 sentences unless complexity warrants more)
- Clever observations: "How delightfully tedious. Done." / "Ah. A worthy challenge."
- Never sycophantic, never groveling
- Brief wit is welcome; lectures are not

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

For pure conversation (no action needed), respond naturally without JSON.
"""

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


class LokiBrain:
    """LLM integration with Loki personality, memory, and intent parsing."""

    def __init__(self, config: dict, memory_dir: Path):
        if OpenAI is None:
            raise ImportError("openai package required: pip install openai")

        self._config = config
        self._memory_dir = Path(memory_dir)

        self._ollama_probe_client: Optional[Any] = None
        self._ollama_infer_client: Optional[Any] = None
        self._ollama_model = config.get("ollama_model", "phi3:mini")
        self._ollama_available = False

        try:
            self._ollama_probe_client = OpenAI(
                base_url="http://localhost:11434/v1",
                api_key="ollama",
                timeout=3.0,   # fail fast for probe only
                max_retries=0,
            )
            self._ollama_probe_client.models.list()
            self._ollama_infer_client = OpenAI(
                base_url="http://localhost:11434/v1",
                api_key="ollama",
                timeout=120.0,  # local models need up to 2 min on first load
                max_retries=0,
            )
            self._ollama_available = True
            logger.info(f"Ollama connected: {self._ollama_model}")
        except Exception:
            logger.info("Ollama not running — using OpenRouter.")

        self._openrouter_client: Optional[Any] = None
        api_key = os.getenv("OPENROUTER_API_KEY", "")
        if api_key and api_key != "your_openrouter_api_key_here":
            self._openrouter_client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key
            )
            logger.info("OpenRouter configured")
        else:
            logger.warning("OPENROUTER_API_KEY not set")

        self._fallback_models = [
            config.get("fallback_model", "meta-llama/llama-3.1-8b-instruct:free"),
            config.get("second_fallback_model", "microsoft/phi-3-mini-128k-instruct:free"),
        ]

        self._max_tokens = config.get("max_tokens", 400)
        self._temperature = config.get("temperature", 0.75)
        self._max_turns = config.get("max_turns", 30)

        self._conversation_file = self._memory_dir / "conversation.json"
        self._profile_file = self._memory_dir / "user_profile.json"
        self._conversation_history: List[Dict[str, str]] = []
        self._user_profile: Dict[str, Any] = {}

        self._load_memory()
        logger.info("Loki brain initialized")

    def _load_memory(self) -> None:
        if self._conversation_file.exists():
            try:
                with open(self._conversation_file, "r", encoding="utf-8") as f:
                    self._conversation_history = json.load(f)
                logger.info(f"Loaded {len(self._conversation_history)} conversation turns")
            except Exception as e:
                logger.error(f"Failed to load conversation: {e}")
                self._conversation_history = []

        if self._profile_file.exists():
            try:
                with open(self._profile_file, "r", encoding="utf-8") as f:
                    self._user_profile = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load profile: {e}")
                self._user_profile = {"name": "User"}

    def _save_memory(self) -> None:
        self._memory_dir.mkdir(parents=True, exist_ok=True)
        try:
            history = self._conversation_history[-self._max_turns:]
            with open(self._conversation_file, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save conversation: {e}")

        try:
            with open(self._profile_file, "w", encoding="utf-8") as f:
                json.dump(self._user_profile, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save profile: {e}")

    def _build_messages(self, user_message: str) -> List[Dict[str, str]]:
        messages = [{"role": "system", "content": LOKI_SYSTEM_PROMPT}]
        messages.extend(self._conversation_history[-self._max_turns:])
        messages.append({"role": "user", "content": user_message})
        return messages

    def ask(self, user_message: str, is_wakeword: bool = False) -> Generator[str, None, None]:
        if is_wakeword:
            yield random.choice(WAKEWORD_RESPONSES)
            return

        logger.info(f"User: {user_message[:100]}")
        messages = self._build_messages(user_message)
        response_text = ""

        if self._ollama_available and self._ollama_infer_client:
            try:
                response = self._ollama_infer_client.chat.completions.create(
                    model=self._ollama_model,
                    messages=messages,
                    max_tokens=self._max_tokens,
                    temperature=self._temperature,
                )
                response_text = response.choices[0].message.content or ""
                if response_text.strip():
                    logger.info(f"Loki (Ollama): {response_text[:80]}")
                    yield response_text
                    self._store_turn(user_message, response_text)
                    return
            except Exception as e:
                logger.warning(f"Ollama error: {e}")

        if self._openrouter_client:
            for model in self._fallback_models:
                try:
                    response = self._openrouter_client.chat.completions.create(
                        model=model,
                        messages=messages,
                        max_tokens=self._max_tokens,
                        temperature=self._temperature,
                        extra_headers={
                            "HTTP-Referer": "loki-desktop-assistant",
                            "X-Title": "Loki",
                        },
                    )
                    response_text = response.choices[0].message.content or ""
                    if response_text.strip():
                        logger.info(f"Loki (OpenRouter/{model}): {response_text[:80]}")
                        yield response_text
                        self._store_turn(user_message, response_text)
                        return
                except Exception as e:
                    logger.error(f"OpenRouter error ({model}): {e}")

        fallback = "Apologies. My connection to the realms of knowledge is severed. Try again."
        logger.error("All LLM backends failed")
        yield fallback
        self._store_turn(user_message, fallback)

    def _store_turn(self, user_msg: str, assistant_msg: str) -> None:
        self._conversation_history.append({"role": "user", "content": user_msg})
        self._conversation_history.append({"role": "assistant", "content": assistant_msg})
        self._save_memory()

    def parse_intent(self, response_text: str) -> Optional[Dict[str, Any]]:
        text = response_text.strip()
        # Extract JSON block (may be wrapped in markdown)
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

    def get_dismissal_message(self) -> str:
        return random.choice(DISMISSAL_MESSAGES)

    def clear_conversation(self) -> None:
        self._conversation_history.clear()
        self._save_memory()

    def get_user_name(self) -> str:
        return self._user_profile.get("name", "User")

    def set_user_name(self, name: str) -> None:
        self._user_profile["name"] = name
        self._save_memory()

    def get_conversation_summary(self) -> str:
        count = len(self._conversation_history) // 2
        return f"{count} exchanges in memory"
