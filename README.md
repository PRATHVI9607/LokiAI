# LOKI — AI Desktop Assistant

> *"The god of mischief, at your service."*

[![CI](https://github.com/PRATHVI9607/LokiAI/actions/workflows/ci.yml/badge.svg)](https://github.com/PRATHVI9607/LokiAI/actions/workflows/ci.yml)

Loki is an elite AI desktop assistant for Windows. Voice-activated, always-on, and deeply integrated with your system — with the wit and competence of a Norse trickster god.

**50+ features** covering OS control, coding, writing, research, security, and productivity — and it **learns from how you use it**.

<!--
  DEMO: record a 15-30s clip (wake word → a command → a spoken reply), save it as
  docs/demo.gif, then replace this comment with:  ![Loki demo](docs/demo.gif)
  Quick capture on Windows: ScreenToGif (free) → export GIF, keep it under ~8 MB.
-->
<p align="center"><em>▶︎ Demo GIF coming soon — see docs/DEMO.md for how it's captured.</em></p>

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
| **App Launcher** | Open **any** installed app by name (alias → PATH → Start-Menu shortcut search) |
| **Computer Control** | Operate the PC like a person: click, type, hotkeys, scroll, read the screen (OCR), click on-screen text by name |
| **Multi-step Automation** | Chains actions: *"open notepad, type my address, save it as address.txt"* — plans and runs the whole sequence |
| **Volume Control** | Set / query system volume (pycaw, Windows API) |
| **Brightness Control** | Set / query screen brightness |
| **Wi-Fi / Bluetooth** | Toggle adapters with one command |
| **Window Tiler** | Snap or tile windows: left/right/quarters/grid (ctypes, no extra deps) |
| **Dynamic UI** | Time-based wallpaper + theme switching (dawn/day/evening/night); mood themes; ctypes wallpaper API |
| **File Watcher** | Polling-based watcher: auto-backup files on change, auto-convert media dropped into an inbox folder |
| **Clipboard Sync** | Mobile clipboard sync — HTTP server on :7778, open in phone browser, no app install needed |

### Coding & Development

| Feature | Description |
|---------|-------------|
| **Bug Analyzer** | LLM-powered code review for any file |
| **Refactoring Advisor** | Identify code smells and get per-issue refactored alternatives |
| **Commit Message Gen** | Reads `git diff`, writes the message |
| **README Generator** | Documents your entire project automatically |
| **Regex Generator** | Describe in English, get the pattern |
| **SQL Builder** | Natural language to SQL query |
| **Code Converter** | Python → Go → TypeScript, any pair |
| **Security Scanner** | Detect API keys, passwords, secrets in code |
| **Git Helper** | Status, commit, diff summaries, **push/pull/remote** (SSH + HTTPS) — push is confirmation-gated |
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
| **Screenshot Search** | Capture screen, OCR text via Windows WinRT / pytesseract, search on-screen content |
| **Screen Translator** | Capture → OCR → translate all visible text to any language |

### Productivity

| Feature | Description |
|---------|-------------|
| **Task Manager** | Add, list, complete tasks; **recurring tasks** (daily/weekly/monthly); validated due dates; AI-ranked priority via LLM scoring |
| **Calendar Manager** | Parse `.ics` files, detect scheduling conflicts, suggest free meeting slots |
| **Expense Tracker** | Extract billing info from email text / `.eml` files; CSV ledger + monthly summary |
| **Focus Mode** | Block distracting sites (YouTube, Reddit, etc.) via hosts file |
| **Clipboard History** | Track and restore clipboard entries |
| **Encrypted Vault** | AES-256-GCM secure key-value secret store |
| **Backup Manager** | Timestamped file and directory backups; auto-trigger on file change via File Watcher |
| **Digital Declutter** | Find duplicate files (MD5), large files, and files not touched in N days |
| **Meeting Transcriber** | Whisper-based transcription + structured minutes generation |
| **Google (Gmail + Calendar)** | *"What's on my calendar today?"*, *"any new email?"*, *"when's my next meeting?"* — live read of your real Google account (one-time OAuth, see below) |

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
| **Phishing Detector** | Heuristic + LLM analysis of URLs and email text for phishing signals |
| **Deepfake Detector** | EXIF absence, GAN dimension heuristics + LLM verdict for AI-generated media |
| **Footprint Auditor** | Audit startup entries, scheduled tasks, privacy settings, network listeners |
| **Code Security Scanner** | Detect secrets and vulnerabilities in source files |
| **Encrypted Vault** | PBKDF2 (310 000 iterations) + AES-256-GCM secret storage |

### 🧠 Intelligence & Learning

| Feature | Description |
|---------|-------------|
| **Proactive Intelligence** | Speaks up unprompted — high CPU/RAM, low battery/disk, long work sessions, late-night nudges (cooldowns, only when idle) |
| **Vision** | *"What's on my screen?"*, *"what's this error?"* — a real vision model reads your screen, with OCR + text-LLM fallback |
| **Streaming Voice** | Splits replies into sentences so the first words start almost instantly; **barge-in** — interrupt mid-sentence |
| **Learning Loop** | Every interaction is logged with outcome + latency + 👍/👎; a **contextual bandit** learns which LLM provider is fastest/most reliable on *your* machine and reorders them |
| **Insights Dashboard** | Live success rate, feedback tally, per-provider reward bars, and a recent-action log with one-click undo |
| **Second Brain** | *"Remember that…"* / *"What did I say about…"* — personal long-term memory with semantic recall (nomic-embed) and keyword fallback |
| **Google (Gmail + Calendar)** | Read inbox/calendar, send email, create events — your real account via OAuth |
| **Spotify** | *"What's playing?"*, *"play …"*, pause/skip — via the Spotify Web API |

---

## Quick Start (Windows)

### CPU — works anywhere (Python 3.10+)

```bash
# Install deps (CPU PyTorch)
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r loki/requirements.txt

# Configure keys
copy loki\.env.example loki\.env
# Edit loki\.env — add OPENROUTER_API_KEY and/or NVIDIA_API_KEY

# Run
python main.py
```

### GPU — faster voice (NVIDIA + uv + Python 3.12)

PyTorch's CUDA wheels need Python 3.11/3.12 (not 3.14). Use [`uv`](https://github.com/astral-sh/uv):

```bash
uv venv --python 3.12 .venv-gpu
uv pip install --python .venv-gpu/Scripts/python.exe torch --index-url https://download.pytorch.org/whl/cu121
uv pip install --python .venv-gpu/Scripts/python.exe -r loki/requirements.txt

# Run on the GPU
run-gpu.bat
```

Then open **http://localhost:7777**. Whisper auto-detects the GPU (`whisper.device: auto`); the terminal shows `(cuda)` when the GPU is active, `(cpu)` otherwise — **either way it runs**.

---

## Configuration

Loki tries providers **fast-first**: local Ollama → NVIDIA NIM (Kimi K2.6) → OpenRouter → Ollama fallback model. Put keys in `loki/.env`:

```env
OPENROUTER_API_KEY=sk-or-...      # free at openrouter.ai/keys
NVIDIA_API_KEY=nvapi-...          # free at build.nvidia.com — serves Kimi K2.6
```

**Local models (recommended — no quota, no network):** run `ollama serve`, then
`ollama pull qwen2.5-coder:7b` (primary) and `ollama pull phi3:mini` (GPU-fast fallback).
For file search/RAG also `ollama pull nomic-embed-text`.

`config.yaml` lets you tune the model chain, `prefer_local`, `ollama_fallback_model`,
`ollama_timeout`, and `whisper.device` (auto/cuda/cpu).

### Google (Gmail + Calendar) — one-time OAuth

Loki reads your **real** calendar and inbox once you connect your Google account. This
is optional — without it, calendar/email commands just reply with these setup steps and
nothing else breaks. To activate:

1. Open [console.cloud.google.com](https://console.cloud.google.com) → create a project.
2. **APIs & Services → Enable APIs** → enable **Gmail API** and **Google Calendar API**.
3. **Credentials → Create Credentials → OAuth client ID → Desktop app**. Download the JSON.
4. Save it as `loki/credentials/google_credentials.json`.
5. Ask Loki *"what's on my calendar today?"* — a browser opens once for consent; the token
   is cached at `loki/credentials/google_token.json` so you only authorize once.

Both files are gitignored. Scopes: `calendar.events` (read + create events),
`gmail.readonly` (read inbox), `gmail.send` (send mail). If you authorized an
earlier read-only build, delete `loki/credentials/google_token.json` and
re-consent so the new scopes take effect.

### Spotify — optional

*"What's playing?"*, *"play bohemian rhapsody"*, *"pause"*, *"skip"*.

1. [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard) → create an app.
2. Add redirect URI `http://localhost:8888/callback`.
3. Put the credentials in `loki/.env`:
   ```env
   SPOTIFY_CLIENT_ID=...
   SPOTIFY_CLIENT_SECRET=...
   ```
4. First use opens a browser to authorize once. Playback control needs Spotify
   Premium; *"what's playing"* works on free too.

### Learning loop (bandit)

Loki logs every interaction to `memory/outcomes.jsonl` (gitignored) and a
contextual bandit reorders cloud LLM providers by the reward it learns from your
own usage. Tune it under `llm.bandit` in `config.yaml` (`enabled`, `epsilon`).
Your local model stays pinned first when `prefer_local` — only the cloud
fallbacks are reordered. Rate replies with 👍/👎 to sharpen it faster.

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
│   ├── brain.py           LLM + KORTEX context engineering (Ollama/OpenRouter); _llm_lock
│   ├── bandit.py          Contextual bandit — learns the best provider from outcomes
│   ├── outcome_log.py     Per-interaction training data (transcript→provider→👍/👎)
│   ├── brain_memory.py    Persistent facts, personality, session summaries (bounded)
│   ├── listener.py        Whisper STT (worker watchdog + explicit stream cleanup)
│   ├── wakeword.py        "Hey Loki" detection (availability-gated)
│   ├── tts.py             edge-tts (Microsoft Neural voices); sentence streaming + barge-in
│   ├── action_router.py   Intent dispatch — 120+ handlers; destructive-op confirmation gate
│   ├── undo_stack.py      Reversible actions (25-deep)
│   ├── memory.py          Persistent conversation + tasks (recurrence, validated dates)
│   ├── audit.py           Structured audit log (UTC-ms) for all actions
│   ├── prompt_utils.py    wrap_untrusted() — prompt-injection defense
│   ├── paths.py           Shared path-traversal validation
│   ├── log_utils.py       Secret redaction for logs
│   ├── config_check.py    Startup config validation
│   └── proactive_monitor  Unprompted "alive" alerts (CPU/RAM/battery/breaks)
├── features/              44 feature modules
│   ├── OS & System        file_search, system_monitor, process_manager, process_triage,
│   │                      file_organizer, window_tiler, dynamic_ui, file_watcher, clipboard_sync
│   ├── Intelligence       web_summarizer, pdf_chat, rag_engine, screenshot_search (vision),
│   │                      semantic_browser_history, knowledge_graph (pruned), fact_checker, second_brain
│   ├── Coding             code_assistant, git_helper (SSH/HTTPS), security_scanner, api_mocker, env_setup
│   ├── Writing            ghostwriter, grammar_polisher, citation_generator,
│   │                      email_drafter, daily_briefing
│   ├── Data               currency_converter, news_aggregator (cached), media_converter,
│   │                      calendar_manager, expense_tracker
│   ├── Integrations       google_integration (Gmail+Calendar), spotify_integration
│   ├── Files              backup_manager, digital_declutter, software_updater
│   ├── Security           vault (throttled), phishing_detector, footprint_auditor
│   ├── Meetings           meeting_transcriber
│   └── Productivity       task_manager, focus_mode, clipboard_manager
├── actions/               6 system action modules (file_ops, shell_exec, system_ctrl,
│                          app_ctrl, browser_ctrl, computer_control)
├── features/auto_agent    multi-step automation planner (chains actions)
├── core/voice_pipeline    exclusive-mic wakeword↔listener handoff
├── core/conversation_sm   conversation state machine (idle/listening/thinking/speaking)
└── ui/                    FastAPI server + Next.js frontend (Norse dark theme)
```

---

## Quality, Testing & Security

- **Tests:** `129` pytest + `6` Vitest, all green. Run with `pytest loki/tests/ -q`
  and (in `loki-ui/`) `npm run typecheck && npm test`.
- **CI:** GitHub Actions runs pytest on Windows + typecheck/Vitest/build on every push.
- **Security hardening:**
  - Prompt-injection defense — untrusted content (web/PDF/screen/email) is delimited
    and the model is told to treat it as data (`prompt_utils.wrap_untrusted`).
  - Path-traversal blocked via a single `paths.resolve_within_roots` check.
  - Vault brute-force throttling; shell allowlist + metacharacter blocking.
  - Rate limiting on the WebSocket + uploads; secrets redacted from logs.
  - Destructive ops (delete, kill, shell, `git push`) require explicit confirmation.
- **Observability:** opt-in JSON logs (`logging.json: true`), a `/stats` endpoint with
  per-provider latency/success, and an in-app **Insights** dashboard.

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
| UI | Next.js 15 (App Router) + FastAPI WebSocket |
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

**Screenshot OCR returns nothing** — Windows OCR requires Windows 10 1809+. Install optional: `pip install pytesseract` and [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) for better accuracy.

**Calendar features need an ICS file** — Export from Google Calendar (Settings → Export) or Outlook (File → Open & Export → Import/Export).

**Clipboard sync not reachable on phone** — Ensure both devices are on the same Wi-Fi network. Check Windows Firewall allows port 7778.

---

## Hardware

Developed on: RTX 2050 (4 GB VRAM), 16 GB RAM, Windows 11.  
Whisper runs on CPU — no dedicated GPU needed.
