# LOKI — AI Desktop Assistant

> *"The god of mischief, at your service."*

Loki is an elite AI desktop assistant for Windows. Voice-activated, always-on, and deeply integrated with your system — with the wit and competence of a Norse trickster god.

**50+ features** covering OS control, coding, writing, research, security, and productivity.

---

## Features

### OS & System Mastery

| Feature | Description |
|---------|-------------|
| **File Search** | Natural-language file search: *"find the PDF I edited last week about ML"* |
| **System Monitor** | CPU, RAM, GPU, disk stats with critical alert thresholds |
| **Process Manager** | List, kill, or suspend background processes |
| **Process Triage** | Auto-close non-essential apps to free resources before gaming/rendering |
| **File Organizer** | Auto-sort Downloads/Desktop by file type |
| **App Launcher** | Open any app by name via voice or text |
| **Volume Control** | Set / query system volume (pycaw, Windows API) |
| **Brightness Control** | Set / query screen brightness |
| **Wi-Fi / Bluetooth** | Toggle adapters with one command |
| **Window Tiler** | Snap or tile windows: left/right/quarters/grid (ctypes, no extra deps) |

### Coding & Development

| Feature | Description |
|---------|-------------|
| **Bug Analyzer** | LLM-powered code review for any file |
| **Commit Message Gen** | Reads `git diff`, writes the message |
| **README Generator** | Documents your entire project automatically |
| **Regex Generator** | Describe in English, get the pattern |
| **SQL Builder** | Natural language to SQL query |
| **Code Converter** | Python → Go → TypeScript, any pair |
| **Security Scanner** | Detect API keys, passwords, secrets in code |
| **Git Helper** | Status, commit, diff summaries |
| **Dockerfile Generator** | Production-ready multi-stage Dockerfile for any project |
| **Venv Setup Script** | PowerShell setup script for Python virtual environments |
| **Docker Compose Gen** | Multi-service docker-compose.yml with healthchecks |
| **API Mock Generator** | LLM-generated mock API server + sample data |

### Writing & Text

| Feature | Description |
|---------|-------------|
| **GhostWriter** | Expand notes to paragraphs, continue writing, bullets → prose |
| **Grammar Polisher** | Fix grammar, change tone (formal/casual/persuasive/academic) |
| **Text Translator** | Translate any text to any language via LLM |
| **Citation Generator** | APA / MLA / Chicago / IEEE citations from URL or manual info |
| **Email Drafter** | Draft professional emails from subject + context |
| **Email Reply** | Generate contextual replies to email threads |
| **Fact Checker** | Web-search + LLM verdict for any claim |

### Research & Web

| Feature | Description |
|---------|-------------|
| **Web Summarizer** | TL;DR any URL in seconds |
| **PDF Chat** | Ask questions about any local PDF document |
| **News Aggregator** | RSS-based headlines from tech, science, world, business, and sports |
| **Daily Briefing** | Morning brief: tasks + system health + news + date/time |
| **Browser History Search** | Keyword and semantic (LLM) search over Chrome/Edge/Brave history |
| **Knowledge Graph** | Extract entities and relationships from notes/files; query via LLM |

### Productivity

| Feature | Description |
|---------|-------------|
| **Task Manager** | Add, list, prioritize, and complete tasks via voice |
| **Focus Mode** | Block distracting sites (YouTube, Reddit, etc.) via hosts file |
| **Clipboard History** | Track and restore clipboard entries |
| **Encrypted Vault** | AES-256-GCM secure key-value secret store |
| **Backup Manager** | Timestamped file and directory backups |
| **Digital Declutter** | Find duplicate files (MD5), large files, and files not touched in N days |
| **Meeting Transcriber** | Whisper-based transcription + structured minutes generation |

### Media & Files

| Feature | Description |
|---------|-------------|
| **Media Converter** | Convert video/audio/image formats via ffmpeg (optional) |
| **Currency Converter** | Live exchange rates via open.er-api.com + LLM fallback |
| **Unit Converter** | Full SI unit table: length, mass, temperature, volume, speed, data |
| **Software Updater** | Check and apply Windows updates via winget |

### Security & Privacy

| Feature | Description |
|---------|-------------|
| **Phishing Detector** | Heuristic + LLM analysis of URLs and email text |
| **Footprint Auditor** | Audit startup entries, scheduled tasks, privacy settings, network listeners |
| **Code Security Scanner** | Detect secrets and vulnerabilities in source files |
| **Encrypted Vault** | PBKDF2 (310 000 iterations) + AES-256-GCM secret storage |

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

# Install PyTorch (CPU build)
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

Loki uses **Ollama locally first** (if running) and falls back to OpenRouter cloud. No GPU required — Whisper runs on CPU.

Edit `loki/config.yaml` to customise:

- LLM model (default: `phi3:mini` via Ollama, `mistral-7b` via OpenRouter)
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
│   ├── brain.py           LLM + KORTEX context engineering (Ollama/OpenRouter)
│   ├── brain_memory.py    Persistent facts, personality, session summaries
│   ├── listener.py        Whisper STT
│   ├── wakeword.py        "Hey Loki" detection
│   ├── tts.py             edge-tts (Microsoft Neural voices)
│   ├── action_router.py   Intent dispatch to 70+ handlers
│   ├── undo_stack.py      Reversible actions (25-deep)
│   ├── memory.py          Persistent conversation + task storage
│   └── audit.py           Structured audit log for all actions
├── features/              35 feature modules
├── actions/               5 system action modules (file, shell, system, app, browser)
└── ui/                    FastAPI server + Next.js frontend (Norse dark theme)
```

---

## Requirements

| Requirement | Notes |
|-------------|-------|
| Python 3.10+ | Required |
| Windows 10/11 | ctypes + winreg features are Windows-only |
| RAM 4 GB+ | 8 GB recommended for Whisper base.en |
| Disk ~3 GB | PyTorch + Whisper model cache |
| GPU | Not required (all models run on CPU) |
| ffmpeg | Optional — required only for media conversion |
| winget | Optional — required only for software update features |

---

## Tech Stack

| Component | Library |
|-----------|---------|
| UI | Next.js 14 (App Router) + FastAPI WebSocket |
| LLM | Ollama (local) / OpenRouter (cloud) |
| STT | OpenAI Whisper |
| TTS | edge-tts (Microsoft Neural) |
| System | psutil, pycaw, screen-brightness-control, ctypes |
| Security | cryptography (AES-256-GCM vault) |
| Git | gitpython |
| Web | requests, beautifulsoup4 |
| PDF | PyMuPDF |
| RAG | sentence-transformers + FAISS |

---

## Troubleshooting

**No audio output** — ensure `pygame` installed: `pip install pygame`

**Whisper download on first run** — Whisper downloads the `base.en` model (~140 MB) automatically on first start.

**"Volume control unavailable"** — `pycaw` requires Windows Audio service. Restart it via `services.msc`.

**Focus mode needs admin** — Editing the hosts file requires running Loki as Administrator.

**Wakeword not detecting** — Increase `vad_aggressiveness` (1–3) in `config.yaml`, or reduce background noise.

**Media conversion fails** — Install ffmpeg and add it to PATH: `winget install Gyan.FFmpeg`

**Browser history search fails** — Close Chrome/Edge first; SQLite locks the file while the browser is open.

---

## Hardware

Developed on: RTX 2050 (4 GB VRAM), 16 GB RAM, Windows 11.  
Whisper runs on CPU — no dedicated GPU needed.
