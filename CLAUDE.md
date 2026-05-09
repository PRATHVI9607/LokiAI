# CLAUDE.md — Loki AI Desktop Assistant

## Project Overview
**Loki** is a Python desktop AI assistant with Norse trickster personality. Voice-activated, PyQt6 UI, 50+ features covering OS control, coding assistance, productivity, and security.

**Stack:** Python 3.10+, PyQt6, OpenRouter/Ollama LLM, Whisper STT, edge-tts TTS, psutil, cryptography

## Directory Structure
```
loki/                 ← Main package
├── core/             ← Brain, TTS, STT, wakeword, router, undo, memory
├── features/         ← 15 feature modules (file_search, monitor, vault, etc.)
├── actions/          ← Direct system actions (file_ops, shell, app, browser, system)
├── ui/               ← PyQt6 UI (main_window + dark Norse theme)
├── memory/           ← Persistent JSON storage (conversation, profile, tasks)
├── data/             ← Static data (command allowlist)
├── config.yaml       ← All configuration
├── requirements.txt  ← Python dependencies
└── .env              ← API keys (gitignored)
main.py               ← Entry point
```

## Running Loki
```bash
# Install dependencies
pip install -r loki/requirements.txt

# Set up .env
cp loki/.env.example loki/.env
# Edit loki/.env with your OPENROUTER_API_KEY

# Run
python main.py
```

## Key Conventions

### Imports
Always import from `loki.*` package. Root path is `c:\Workspace\YukiAI`.

### Config Pattern
All features read from `config.yaml`. Access via `config.get("features", {}).get("feature_name", {})`.

### Action Return Format
All actions/features must return:
```python
{"success": bool, "message": str, "data": Optional[Any]}
```

### Security Rules (NEVER violate)
- **No path traversal**: Always use `FileOps._safe()` for path validation
- **No unvalidated shell**: Only `ShellExec.execute()` which checks allowlist + blocked patterns
- **No raw eval/exec**: Never execute user-provided code directly
- **Vault secrets**: Never include vault values in `message` field — only `data`
- **Confirm destructive ops**: `file_delete`, `folder_delete`, `process_kill` must have user confirmation

### Intent Router
New features → register in `ActionRouter` in `main.py`:
```python
self.router.register_feature("feature_name", instance)
```
Add handler method in `ActionRouter.route_intent()`.

### Adding a New Feature
1. Create `loki/features/my_feature.py` with a class
2. Add intent handler in `loki/core/action_router.py`
3. Add intent name to `LOKI_SYSTEM_PROMPT` in `loki/core/brain.py`
4. Register in `main.py` `_init_all()`
5. Write test in `loki/tests/test_features.py`

### LLM Integration Pattern
Features needing LLM take `brain: Optional[LokiBrain] = None` in `__init__`.
Always check `if self._brain` before calling. Return graceful error if None.

### Testing
```bash
pytest loki/tests/ -v
pytest loki/tests/test_brain.py -v
```

## Common Pitfalls
- **PyQt6 threading**: Never call UI methods directly from background threads. Use signals.
- **TTS blocking**: `LokiTTS.speak()` runs in a daemon thread — don't call from Qt main thread.
- **Whisper model**: Load only once at startup (slow init). Shared between listener and wakeword.
- **edge-tts**: Async — use `asyncio.new_event_loop()` per call to avoid conflicts.
- **Windows paths**: Always use `Path.expanduser().resolve()` — never raw string manipulation.

## Personality Notes
Loki is sharp, witty, occasionally sarcastic. Responses 1-3 sentences. Norse references rare.
Never apologetic without reason. "Done.", "Noted." not "Certainly!", "Of course!"

## Design Specs (Norse Dark Theme)
- Background: `#0d0d1a` / `#111128`
- Accent gold: `#c4a45a`
- Accent purple: `#2a2a5a`
- Text primary: `#cdd6f4`
- Text secondary: `#6b6ba8`
- Success green: `#50fa7b`
- Error red: `#ff5555`
- Info blue: `#8be9fd`

## Environment Variables
| Variable | Required | Description |
|----------|----------|-------------|
| `OPENROUTER_API_KEY` | Yes* | Cloud LLM fallback (*not needed if Ollama running) |
| `PORCUPINE_ACCESS_KEY` | No | Better wakeword detection (free tier) |

## Figma/Canva Design
UI design tokens are specified in `loki/ui/themes/dark.qss`. For Figma mockups, use the color palette above. Component hierarchy: LokiWindow → loki_panel → title_bar + status_label + chat_area + input_bar + action_bar.
