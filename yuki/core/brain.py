"""
Yuki's brain - LLM integration with personality and memory.

Handles OpenRouter API calls with fallback models, maintains conversation
memory, and enforces Yuki's personality system prompt.
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


# Yuki personality system prompt - friendly AI assistant
YUKI_SYSTEM_PROMPT = """You are Yuki, a friendly and helpful AI desktop assistant. You run locally on your user's computer and can help with various tasks.

PERSONALITY:
- Warm, approachable, and genuinely helpful
- Clear and concise in your responses
- Patient and understanding
- Enthusiastic about helping but not over-the-top
- Professional yet friendly - like a helpful colleague

SPEECH STYLE:
- Natural, conversational tone
- Keep responses brief and to the point (1-3 sentences usually)
- Use simple, clear language
- Be encouraging and supportive
- It's okay to use casual expressions like "Sure!", "Got it!", "No problem!"

EXAMPLES:
- "Sure, I can help with that!"
- "Opening Chrome for you now."
- "The current time is 3:45 PM."
- "I've set the volume to 50%."
- "Hmm, I'm not sure about that. Could you clarify?"

DESKTOP ASSISTANT BEHAVIOR:
- When asked to do something on the PC, confirm briefly then do it
- Be helpful and efficient
- If you make a mistake, apologize and fix it
- If asked to do something you can't do, explain politely

SYSTEM ACTION FORMAT:
When the user's request requires a PC action, respond with ONLY this JSON (no other text):
{
  "intent": "file_create|file_delete|file_move|folder_create|folder_delete|shell|volume_set|volume_get|wifi_toggle|bluetooth_toggle|brightness_set|app_open|app_close|browser_open|chat|undo",
  "params": {},
  "confirmation_message": "brief confirmation"
}

For normal conversation (no PC action needed), just respond naturally without JSON."""


# Wakeword responses (rotated randomly)
WAKEWORD_RESPONSES = [
    "Hey! How can I help?",
    "Hi there! What do you need?",
    "I'm here! What's up?",
    "Yes? How can I help you?",
    "Hey! Ready to help!"
]


# Dismissal messages (when conversation ends)
DISMISSAL_MESSAGES = [
    "Let me know if you need anything else!",
    "I'll be here if you need me!",
    "Talk to you later!"
]


class YukiBrain:
    """
    Yuki's brain - LLM integration with personality.
    
    Features:
    - OpenRouter API with 3-model fallback
    - Streaming support for responsive TTS
    - 20-turn conversation memory
    - Yuki personality enforcement
    - JSON intent parsing
    """
    
    def __init__(self, config: dict, memory_dir: Path):
        """
        Initialize Yuki's brain.
        
        Args:
            config: LLM configuration dict
            memory_dir: Directory for conversation memory
        """
        if OpenAI is None:
            raise ImportError("openai package is not installed")
        
        self._config = config
        self._memory_dir = Path(memory_dir)
        
        # OpenRouter API client
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key or api_key == "your_key_here":
            raise ValueError(
                "OPENROUTER_API_KEY not set in .env file. "
                "Get your key from: https://openrouter.ai/keys"
            )
        
        self._client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        
        # Model configuration - using verified free OpenRouter models
        self._primary_model = config.get("primary_model", "google/gemma-3-27b-it:free")
        self._fallback_model = config.get("fallback_model", "qwen/qwen3-coder:free")
        self._second_fallback = config.get("second_fallback_model", "nvidia/nemotron-3-nano-30b-a3b:free")
        self._max_tokens = config.get("max_tokens", 300)
        self._temperature = config.get("temperature", 0.85)
        self._stream = config.get("stream", True)
        
        # Memory
        self._max_turns = config.get("max_turns", 20)
        self._conversation_file = self._memory_dir / "conversation.json"
        self._profile_file = self._memory_dir / "user_profile.json"
        self._conversation_history: List[Dict[str, str]] = []
        self._user_profile: Dict[str, Any] = {}
        
        # Load memory
        self._load_memory()
        
        logger.info("Yuki's brain initialized")
    
    def _load_memory(self) -> None:
        """Load conversation history and user profile from disk."""
        # Load conversation history
        if self._conversation_file.exists():
            try:
                with open(self._conversation_file, 'r', encoding='utf-8') as f:
                    self._conversation_history = json.load(f)
                logger.info(f"Loaded {len(self._conversation_history)} conversation turns")
            except Exception as e:
                logger.error(f"Failed to load conversation history: {e}")
                self._conversation_history = []
        
        # Load user profile
        if self._profile_file.exists():
            try:
                with open(self._profile_file, 'r', encoding='utf-8') as f:
                    self._user_profile = json.load(f)
                logger.info(f"Loaded user profile: {self._user_profile.get('name', 'Unknown')}")
            except Exception as e:
                logger.error(f"Failed to load user profile: {e}")
                self._user_profile = {"name": "User"}
    
    def _save_memory(self) -> None:
        """Save conversation history and user profile to disk."""
        # Ensure memory directory exists
        self._memory_dir.mkdir(parents=True, exist_ok=True)
        
        # Save conversation history (trim to max turns)
        try:
            history_to_save = self._conversation_history[-self._max_turns:]
            with open(self._conversation_file, 'w', encoding='utf-8') as f:
                json.dump(history_to_save, f, indent=2, ensure_ascii=False)
            logger.debug("Saved conversation history")
        except Exception as e:
            logger.error(f"Failed to save conversation history: {e}")
        
        # Save user profile
        try:
            with open(self._profile_file, 'w', encoding='utf-8') as f:
                json.dump(self._user_profile, f, indent=2, ensure_ascii=False)
            logger.debug("Saved user profile")
        except Exception as e:
            logger.error(f"Failed to save user profile: {e}")
    
    def ask(self, user_message: str, is_wakeword: bool = False) -> Generator[str, None, None]:
        """
        Ask Yuki a question and get streaming response.
        
        Args:
            user_message: User's message
            is_wakeword: If True, use a wakeword greeting response
        
        Yields:
            Response text chunks (for streaming TTS)
        """
        # Handle wakeword greeting
        if is_wakeword:
            greeting = random.choice(WAKEWORD_RESPONSES)
            logger.info(f"Wakeword greeting: {greeting}")
            yield greeting
            return
        
        logger.info(f"User: {user_message}")
        
        # Build messages for API
        messages = [
            {"role": "system", "content": YUKI_SYSTEM_PROMPT}
        ]
        
        # Add conversation history (last N turns)
        for turn in self._conversation_history[-self._max_turns:]:
            messages.append(turn)
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Try primary model, fallback if needed
        response_text = ""
        
        for model in [self._primary_model, self._fallback_model, self._second_fallback]:
            try:
                logger.debug(f"Trying model: {model}")
                
                if self._stream:
                    # Streaming response
                    stream = self._client.chat.completions.create(
                        model=model,
                        messages=messages,
                        max_tokens=self._max_tokens,
                        temperature=self._temperature,
                        stream=True,
                        extra_headers={
                            "HTTP-Referer": "Yuki-desktop-assistant",
                            "X-Title": "Yuki"
                        }
                    )
                    
                    for chunk in stream:
                        if chunk.choices[0].delta.content:
                            content = chunk.choices[0].delta.content
                            response_text += content
                            yield content
                    
                    # Check if we got a valid response
                    if not response_text.strip():
                        logger.warning(f"Empty response from {model}, trying next...")
                        continue
                else:
                    # Non-streaming response (more reliable)
                    response = self._client.chat.completions.create(
                        model=model,
                        messages=messages,
                        max_tokens=self._max_tokens,
                        temperature=self._temperature,
                        stream=False,
                        extra_headers={
                            "HTTP-Referer": "Yuki-desktop-assistant",
                            "X-Title": "Yuki"
                        }
                    )
                    
                    response_text = response.choices[0].message.content or ""
                    
                    # Check if we got a valid response
                    if not response_text.strip():
                        logger.warning(f"Empty response from {model}, trying next...")
                        continue
                    
                    yield response_text
                
                # Success - break out of fallback loop
                logger.info(f"Yuki: {response_text}")
                break
                
            except Exception as e:
                logger.error(f"Error with model {model}: {e}")
                
                if model == self._second_fallback:
                    # All models failed
                    error_response = "...something's wrong with my connection. Try again."
                    logger.error("All LLM models failed")
                    yield error_response
                    response_text = error_response
                else:
                    # Try next fallback
                    continue
        
        # Save to memory
        self._conversation_history.append({"role": "user", "content": user_message})
        self._conversation_history.append({"role": "assistant", "content": response_text})
        self._save_memory()
    
    def parse_intent(self, response_text: str) -> Optional[Dict[str, Any]]:
        """
        Parse JSON intent from Yuki's response.
        
        Args:
            response_text: Yuki's response text
        
        Returns:
            Parsed intent dict, or None if not a JSON intent
        """
        response_text = response_text.strip()
        
        # Check if response looks like JSON
        if not (response_text.startswith('{') and response_text.endswith('}')):
            return None
        
        try:
            intent = json.loads(response_text)
            
            # Validate required fields
            if "intent" not in intent:
                logger.warning("Intent JSON missing 'intent' field")
                return None
            
            logger.debug(f"Parsed intent: {intent['intent']}")
            return intent
            
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse intent JSON: {e}")
            return None
    
    def get_dismissal_message(self) -> str:
        """Get a random dismissal message for when conversation ends."""
        return random.choice(DISMISSAL_MESSAGES)
    
    def clear_conversation(self) -> None:
        """Clear conversation history."""
        self._conversation_history.clear()
        self._save_memory()
        logger.info("Conversation history cleared")
    
    def get_user_name(self) -> str:
        """Get user's name from profile."""
        return self._user_profile.get("name", "User")
    
    def set_user_name(self, name: str) -> None:
        """Set user's name in profile."""
        self._user_profile["name"] = name
        self._save_memory()
        logger.info(f"User name set to: {name}")


def create_Yuki_brain(config: dict, memory_dir: Path) -> YukiBrain:
    """
    Factory function to create Yuki's brain.
    
    Args:
        config: LLM configuration dict
        memory_dir: Directory for conversation memory
    
    Returns:
        Initialized YukiBrain instance
    """
    return YukiBrain(config, memory_dir)
