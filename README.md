# LOKI — AI Desktop Assistant

> *"The god of mischief, at your service."*

Loki is an elite AI desktop assistant for Windows. Named after the Norse trickster god, it combines sharp wit with devastating competence — voice-activated, always-on, and deeply integrated with your system.

## Features

### OS & System Mastery

- **Natural Language File Search** — "find the PDF I edited last week about ML"
- **System Health Monitor** — CPU, RAM, GPU, disk stats with critical alerts
- **Process Manager** — list and kill background processes
- **File Organizer** — auto-sort Downloads/Desktop by file type
- **App Launcher** — open any app by name
- **Volume & Brightness Control** — via voice or text
- **Wi-Fi Toggle** — one command

### Coding & Development

- **Bug Analyzer** — LLM-powered code review for any file
- **Commit Message Generator** — reads git diff, writes the message
- **README Generator** — documents your entire project automatically
- **Regex Generator** — describe it in English, get the pattern
- **SQL Builder** — natural language to SQL query
- **Code Converter** — Python to Go? Done.
- **Security Scanner** — detect API keys, passwords, secrets in your codebase
- **Git Helper** — status, commit, diff summaries

### Web & Research

- **Web Summarizer** — TL;DR any URL in seconds
- **PDF Chat** — ask questions about any local PDF document

### Productivity

- **Task Manager** — add, prioritize, and complete tasks via voice
- **Focus Mode** — block distracting sites (YouTube, Reddit, etc.)
- **Clipboard History** — track and restore clipboard entries
- **Encrypted Vault** — AES-256-GCM secure key-value store

### Security

- All file ops restricted to home directory
- Shell commands filtered through allowlist
- Path traversal prevention on every operation
- Vault uses PBKDF2 (310,000 iterations) + AES-GCM

## Quick Start

```bash
# Install dependencies
pip install -r loki/requirements.txt

# Configure
cp loki/.env.example loki/.env
# Edit .env — add your OPENROUTER_API_KEY

# Run
python main.py
```

## Wake Word

Say **"Hey Loki"** to activate. Loki shows the window and listens.
Or type directly in the chat panel.

## Architecture

```text
main.py                    Entry point — wires everything
loki/
├── core/
│   ├── brain.py           LLM + Loki personality (Ollama/OpenRouter)
│   ├── listener.py        Whisper STT
│   ├── wakeword.py        "Hey Loki" detection
│   ├── tts.py             edge-tts (Microsoft Neural voices)
│   ├── action_router.py   Intent dispatch to 40+ handlers
│   ├── undo_stack.py      Reversible actions (25-deep)
│   └── memory.py          Persistent conversation + task storage
├── features/              15 feature modules
├── actions/               5 system action modules (file, shell, system, app, browser)
└── ui/                    PyQt6 dark Norse theme (purple/gold)
```

## Configuration

Edit `loki/config.yaml`:

- LLM model (Ollama local or OpenRouter cloud)
- TTS voice (default: `en-GB-RyanNeural` — British male)
- Wake word sensitivity
- Focus mode site blocklist
- File organizer rules

## Tech Stack

| Component | Library                                  |
| --------- | ---------------------------------------- |
| UI        | PyQt6 (dark Norse theme)                 |
| LLM       | Ollama (local) / OpenRouter (cloud)      |
| STT       | OpenAI Whisper                           |
| TTS       | edge-tts (Microsoft Neural)              |
| System    | psutil, pycaw, screen-brightness-control |
| Security  | cryptography (AES-256-GCM vault)         |
| Git       | gitpython                                |
| Web       | requests, beautifulsoup4                 |
| PDF       | PyMuPDF                                  |

## Hardware

Developed on: RTX 2050 (4GB VRAM), 16GB RAM, Windows 11.
Whisper runs on CPU; TTS via edge API (no local GPU needed).
