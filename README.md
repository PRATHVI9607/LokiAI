# LOKI — AI Desktop Assistant

> *"The god of mischief, at your service."*

Loki is an elite AI desktop assistant for Windows. Voice-activated, always-on, and deeply integrated with your system — with the wit and competence of a Norse trickster god.

## Features

### OS & System Mastery

- **Natural Language File Search** — "find the PDF I edited last week about ML"
- **System Health Monitor** — CPU, RAM, GPU, disk stats with critical alerts
- **Process Manager** — list and kill background processes
- **File Organizer** — auto-sort Downloads/Desktop by file type
- **App Launcher** — open any app by name
- **Volume & Brightness Control** — via voice or text
- **Wi-Fi / Bluetooth Toggle** — one command

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

- All file operations restricted to home directory
- Shell commands filtered through allowlist
- Path traversal prevention on every operation
- Vault uses PBKDF2 (310,000 iterations) + AES-256-GCM

---

## Quick Start (Windows)

### Option A — One-click installer (recommended)

```bat
git clone https://github.com/PRATHVI9607/LokiAI.git
cd LokiAI
install.bat
```

Then edit `loki\.env` with your API key and run:

```bat
run.bat
```

### Option B — Manual setup

```bash
# Python 3.10+ required
python -m venv venv
venv\Scripts\activate

# Install PyTorch (CPU build — smaller, no GPU needed for Whisper)
pip install torch --index-url https://download.pytorch.org/whl/cpu

# Install Loki dependencies
pip install -r loki/requirements.txt

# Configure
copy loki\.env.example loki\.env
# Edit loki\.env — add your OPENROUTER_API_KEY

# Run
python main.py
```

---

## Configuration

Get a **free** OpenRouter API key at [openrouter.ai/keys](https://openrouter.ai/keys) and put it in `loki/.env`:

```env
OPENROUTER_API_KEY=sk-or-...
```

Loki uses **Ollama locally first** (if you have it running) and falls back to OpenRouter cloud. No GPU required — Whisper runs on CPU.

Edit `loki/config.yaml` to customise:

- LLM model (default: `phi3:mini` via Ollama, `llama-3.1-8b` via OpenRouter)
- TTS voice (default: `en-GB-RyanNeural` — British male Neural voice)
- Wake word sensitivity
- Focus mode site blocklist
- File organizer rules

---

## Wake Word

Say **"Hey Loki"** to activate. Loki shows the window and listens.
Or type directly in the chat panel.

---

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

---

## Requirements

| Requirement | Version                                      |
| ----------- | -------------------------------------------- |
| Python      | 3.10+                                        |
| OS          | Windows 10/11                                |
| RAM         | 4 GB+ (8 GB recommended for Whisper base.en) |
| Disk        | ~3 GB (PyTorch + Whisper model cache)        |
| GPU         | Not required (all models run on CPU)         |

---

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

---

## Troubleshooting

**No audio output** — ensure `pygame` installed: `pip install pygame`

**Whisper download on first run** — Whisper downloads the `base.en` model (~140 MB) automatically on first start.

**"Volume control unavailable"** — `pycaw` requires Windows audio service running. Restart the Windows Audio service.

**Focus mode needs admin** — Editing the hosts file requires running Loki as Administrator.

**Wakeword not detecting** — Increase `vad_aggressiveness` (1–3) in `config.yaml`, or reduce background noise.

---

## Hardware

Developed on: RTX 2050 (4 GB VRAM), 16 GB RAM, Windows 11.
Whisper runs on CPU — no dedicated GPU needed.
