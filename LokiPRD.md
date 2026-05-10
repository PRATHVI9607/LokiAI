# Loki AI — Product Requirements Document

**Version:** 1.0  
**Date:** 2026-05-10  
**Author:** Rakshak Sujith  
**Status:** Living Document

---

## Table of Contents

1. [Product Overview](#1-product-overview)
2. [Vision & Goals](#2-vision--goals)
3. [User Personas](#3-user-personas)
4. [System Architecture](#4-system-architecture)
5. [Core Intelligence Features](#5-core-intelligence-features)
6. [File & Folder Operations](#6-file--folder-operations)
7. [System Control Features](#7-system-control-features)
8. [Developer Tools](#8-developer-tools)
9. [Productivity Features](#9-productivity-features)
10. [Security & Privacy Features](#10-security--privacy-features)
11. [Voice Interface](#11-voice-interface)
12. [Web UI](#12-web-ui)
13. [API Reference](#13-api-reference)
14. [Configuration Reference](#14-configuration-reference)
15. [Data Persistence & Storage](#15-data-persistence--storage)
16. [Security Constraints & Safety Model](#16-security-constraints--safety-model)
17. [Dependencies & Requirements](#17-dependencies--requirements)
18. [Extended Feature Set (v1.1)](#18-extended-feature-set-v11)

---

## 1. Product Overview

**Loki** is a local-first AI desktop assistant for Windows, built around a Norse trickster personality. It combines a large language model backend (local via Ollama or cloud via OpenRouter) with deep OS integration, giving users a single conversational interface to control their computer, query knowledge from documents, write and analyze code, manage tasks, and automate everyday workflows — entirely through voice or text.

The assistant runs as a Python backend exposing a FastAPI/WebSocket server, with a Next.js frontend served from the same process. Every feature is voice-activated and designed for low latency.

**Key differentiators:**
- Fully local option — Ollama + Whisper + local embeddings, no cloud required
- 50+ built-in capabilities exposed through natural language
- Persistent memory across sessions (facts, preferences, summaries)
- RAG (Retrieval-Augmented Generation) over user-uploaded documents
- Role-based personality switching (Loki / Jarvis / Friday)
- Hard security boundaries — no path traversal, no unvalidated shell execution, no secrets in logs

---

## 2. Vision & Goals

### Vision
A desktop AI that feels like a knowledgeable colleague who has full access to your machine: able to act on it, remember things about you, and respond in < 2 seconds for simple commands.

### Primary Goals
| # | Goal | Success Metric |
|---|------|---------------|
| G1 | Reduce time to complete repetitive OS tasks | 5-click tasks done in 1 voice command |
| G2 | Keep all user data local by default | Zero cloud calls when Ollama is running |
| G3 | Persistent, growing understanding of the user | Fact extraction auto-runs every 5 exchanges |
| G4 | Natural language as the sole interface | Every capability reachable via voice or text |
| G5 | Security without friction | All destructive ops require confirmation; secrets never appear in logs |

### Non-Goals
- This is not a multi-user SaaS product
- Loki does not replace a full IDE or operating system
- Mobile and macOS/Linux are out of scope (Windows-specific APIs used throughout)

---

## 3. User Personas

### Primary: The Power User Developer
- Writes code daily, wants quick OS automation without leaving their workflow
- Values speed and terseness over hand-holding
- Wants code review, commit messages, and README generation on demand

### Secondary: The Personal Productivity User
- Uses the computer for work, creative projects, and media consumption
- Wants to manage files, tasks, and apps through voice while hands are busy
- Appreciates clipboard history, focus mode, and vault for password storage

### Tertiary: The Privacy-Conscious User
- Prefers all computation to stay local
- Uses Ollama exclusively, never sends data to OpenRouter
- Stores sensitive information in the encrypted vault rather than cloud services

---

## 4. System Architecture

Loki is composed of five layers. The voice pipeline, the web UI, and the Python backend all converge on a single WebSocket channel at port 7777.

### 4.1 High-Level System Overview

```mermaid
graph TD
    subgraph Input["Input Layer"]
        MIC["🎙 Microphone\nsounddevice 16kHz"]
        UI["🌐 Next.js Frontend\nport 7777"]
    end

    subgraph Voice["Voice Pipeline"]
        WW["Wakeword Detector\nWhisper tiny.en\n'Hey Loki' + variants"]
        STT["Speech-to-Text\nWhisper base.en"]
    end

    subgraph Server["FastAPI Server  loki/ui/server.py"]
        WS["/ws  WebSocket"]
        REST["REST Endpoints\n/upload · /files · /brain\n/health · /audit"]
    end

    subgraph Core["Core Intelligence"]
        BRAIN["🧠 Brain\nLLM Engine"]
        AR["Action Router\nintent → handler"]
        MEM["Brain Memory\nbrain.json"]
        RAG["RAG Engine\nnomic-embed-text"]
        TTS["TTS Engine\nedge-tts / pyttsx3"]
        UNDO["Undo Stack\nmax 25 entries"]
        AUDIT["Audit Log\naudit.jsonl"]
    end

    subgraph LLM["LLM Backends"]
        OL["Ollama\nlocalhost:11434\nphi3:mini"]
        OR["OpenRouter\ncloud fallback"]
    end

    subgraph Handlers["Action Handlers"]
        FO["File Ops\ncreate · delete\nmove · read · search"]
        SC["System Ctrl\nvolume · brightness\nwifi · bluetooth"]
        SH["Shell Exec\nallowlist + blocklist"]
        AC["App & Browser\nopen · close · search"]
        FT["15 Feature Modules\nRAG · vault · tasks\nfocus · git · code…"]
    end

    subgraph Storage["Local Storage"]
        DISK[("📁 loki/memory/\nbrain.json\ntasks.json\nvault.enc\nrag_index.json\naudit.jsonl")]
    end

    MIC --> WW --> STT --> WS
    UI <-->|"WebSocket + HTTP"| WS
    UI <-->|"REST"| REST

    WS --> BRAIN
    BRAIN <-->|"facts · summaries"| MEM
    BRAIN <-->|"embed · retrieve"| RAG
    BRAIN -->|"intent JSON"| AR
    BRAIN -->|"plain text reply"| WS
    BRAIN -->|"LLM call"| OL
    BRAIN -.->|"fallback"| OR

    AR --> FO & SC & SH & AC & FT
    FO & SC & SH & AC & FT -->|"result dict"| WS
    FO & SC --> UNDO
    FO & SC & SH & FT --> AUDIT

    WS -->|"speak"| TTS
    MEM <--> DISK
    RAG <--> DISK
    AUDIT --> DISK
```

---

### 4.2 Full Request Processing Flow

This sequence shows the complete lifecycle of a single user request from voice to response.

```mermaid
sequenceDiagram
    actor User
    participant WW as Wakeword<br/>Detector
    participant STT as Whisper<br/>STT
    participant WS as WebSocket<br/>Server
    participant Brain as Brain<br/>(LLM)
    participant RAG as RAG<br/>Engine
    participant Mem as Brain<br/>Memory
    participant AR as Action<br/>Router
    participant Handler as Feature/<br/>Action
    participant TTS as TTS<br/>Engine

    User->>WW: "Hey Loki, set volume to 40"
    WW-->>WS: status: listening
    WS-->>User: 🟡 Listening...
    WW->>STT: activate full transcription
    STT-->>WS: transcript: "set volume to 40"
    WS-->>User: live transcript shown

    WS->>Brain: process("set volume to 40")
    Brain-->>WS: status: thinking
    WS-->>User: 🔵 Thinking...

    Brain->>Mem: fetch facts + personality
    Mem-->>Brain: context payload
    Brain->>RAG: embed query → top-5 chunks
    RAG-->>Brain: relevant document context

    Brain->>Brain: construct KORTEX prompt<br/>(system + memory + RAG + history + query)
    Brain->>Brain: call Ollama (phi3:mini)
    Brain-->>Brain: intent JSON {"intent":"volume_set","params":{"percent":40}}

    Brain->>AR: dispatch intent
    AR->>Handler: SystemCtrl.volume_set(40)
    Handler->>Handler: pycaw COM → SetMasterVolumeLevelScalar
    Handler->>Handler: push to undo stack
    Handler->>Handler: write audit log (tier 2)
    Handler-->>AR: {success:true, message:"Volume set to 40%"}
    AR-->>Brain: result

    Brain-->>WS: loki_message: "Volume set to 40%"
    WS-->>User: 💬 message bubble appears
    WS->>TTS: speak("Volume set to 40%")
    TTS-->>User: 🔊 audio plays
    WS-->>User: status: idle
```

---

### 4.3 LLM Fallback Chain

```mermaid
flowchart TD
    A([User Request]) --> B{Ollama\nrunning?}
    B -->|Yes| C[Call Ollama\nphi3:mini\nlocalhost:11434]
    B -->|No / timeout| D{OPENROUTER_API_KEY\nset?}
    C -->|Success| Z([Return Response])
    C -->|Error| D
    D -->|Yes| E[Call OpenRouter\nPrimary Model]
    D -->|No| F([Return: LLM unavailable])
    E -->|Success| Z
    E -->|Error| G[Call OpenRouter\nSecondary Model]
    G -->|Success| Z
    G -->|Error| F
```

---

### 4.4 Startup & Initialization Sequence

`python main.py` triggers a strict ordered boot. Every component depends on the previous ones being ready.

```mermaid
flowchart TD
    A(["python main.py"]) --> B["Load config.yaml\n+ .env"]
    B --> C["setup_logging()\nfile + stdout handlers"]
    C --> D["_init_all()"]

    subgraph Init["_init_all()  — ordered boot"]
        direction TB
        I1["① UndoStack\nmax_depth from config"]
        I2["② MemoryManager\nloki/memory/ directory"]
        I3["③ BrainMemory\nbrain.json thread-safe store"]
        I4["④ AuditLog\naudit.jsonl append-only"]
        I5["⑤ RagEngine\nnomic-embed-text · rag_index.json"]
        I6["⑥ LokiBrain\nLLM engine + BrainMemory + RagEngine"]
        I7["⑦ TTS Engine\nedge-tts or pyttsx3"]
        I8["⑧ LokiServer\nFastAPI + WebSocket + Static files"]
        I9["⑨ Actions\nFileOps · ShellExec · SystemCtrl\nAppCtrl · BrowserCtrl"]
        I10["⑩ Features (13 modules)\nFileSearch · SystemMonitor · ProcessManager\nWebSummarizer · PDFChat · CodeAssistant\nGitHelper · FocusMode · TaskManager\nClipboardManager · Vault · SecurityScanner\nFileOrganizer"]
        I11["⑪ ActionRouter\nregisters all actions + features"]
        I12["⑫ ConversationManager\nwires Brain + Router + TTS + Server"]
        I13["⑬ SpeechListener\nfull-utterance Whisper STT"]
        I14["⑭ WakewordDetector\ntiny.en · background thread"]
        I1-->I2-->I3-->I4-->I5-->I6-->I7-->I8-->I9-->I10-->I11-->I12-->I13-->I14
    end

    D --> Init
    Init --> E["_wire_callbacks()\nconnect all event handlers"]

    subgraph Callbacks["_wire_callbacks()"]
        direction LR
        C1["wakeword.on_wakeword → start_conversation + listen"]
        C2["wakeword.on_transcript → server.update_transcript"]
        C3["listener.on_transcript → conversation.process_input"]
        C4["tts.on_speaking_started/stopped → server.set_status"]
        C5["server.on_user_message → conversation.process_input"]
        C6["server.on_mute_toggle → wakeword stop/start"]
        C7["server.on_undo → undo_stack.pop_and_undo"]
    end

    E --> Callbacks
    Callbacks --> F["run()\nStart wakeword thread\nRegister lifespan startup handler\nOpen browser (daemon thread +2s)\nuvicorn.run() — blocks main thread"]
    F --> G(["✅ Loki online\nport 7777"])
```

---

### 4.5 Thread Model

Loki runs multiple threads concurrently. Understanding which thread owns which operation is critical for debugging.

```mermaid
graph TD
    subgraph Main["Main Thread  (uvicorn event loop)"]
        UV["uvicorn async event loop\nFastAPI routes + WebSocket handler\nBrain.ask() called here\nRAG embedding called here"]
    end

    subgraph WW["Wakeword Thread  (daemon)"]
        WWT["WakewordDetector.start()\nContinuous audio capture\nsounddevice · 16kHz\nWhisper tiny.en per 2s chunk\nRMS silence filtering"]
    end

    subgraph STT["STT Thread  (daemon, on-demand)"]
        STTT["SpeechListener\nActivated by wakeword callback\nWhisper base.en full transcription\nCallback: conversation.process_input()"]
    end

    subgraph TTS["TTS Thread  (daemon)"]
        TTST["LokiTTS.speak()\nedge-tts asyncio.new_event_loop()\npygame.mixer playback\nCallback: server.set_status() via thread-safe queue"]
    end

    subgraph CB["Clipboard Thread  (daemon)"]
        CBT["ClipboardManager\npyperclip polling loop\n20-item history ring buffer"]
    end

    subgraph BR["Browser Opener  (daemon, one-shot)"]
        BRT["Opens localhost:7777\nafter 2 second delay"]
    end

    WWT -->|"on_wakeword callback\n(calls into main loop)"| UV
    WWT -->|"on_transcript callback"| UV
    STTT -->|"on_transcript callback\n→ process_input"| UV
    TTST -->|"set_status callbacks\n→ WebSocket broadcast"| UV
    CBT -.->|"no direct cross-thread\ncall — history stored locally"| CBT
    BRT -.->|"one-shot at startup"| BRT
```

---

### 4.6 ConversationManager — Internal Processing Flow

`ConversationManager` is the orchestrator that sits between the voice/browser inputs and the Brain/Router. Every user message passes through this flow:

```mermaid
flowchart TD
    IN(["User input\nvoice transcript\nor browser text"]) --> STORE["server.add_user_message()\nPush to chat history"]
    STORE --> STATUS1["server.set_status('thinking')\nBroadcast via WebSocket"]
    STATUS1 --> CLEAR["server.clear_transcript()\nHide live STT strip"]
    CLEAR --> ASK["brain.ask(text)\nGenerator — yields response chunks\nBlocking call on main thread"]
    ASK --> FULL["Accumulate full_response\nfrom generator chunks"]
    FULL --> EMPTY{"full_response\nempty?"}
    EMPTY -->|"Yes"| FALLBACK["Use fallback string\n'That query produced\nnothing of substance.'"]
    EMPTY -->|"No"| PARSE["brain.parse_intent(full_response)\nLook for JSON block\nin LLM output"]

    PARSE --> INTENT{"Intent\nfound?"}
    INTENT -->|"No / intent = chat"| CHAT["server.add_loki_message()\n+ tts.speak()\nPlain text reply"]
    INTENT -->|"Yes"| MSG["Speak intent.message\n(optional pre-action commentary)"]
    MSG --> ROUTE["router.route_intent(intent)\nDispatch to handler"]
    ROUTE --> RESULT["handler returns\n{success, message, data}"]
    RESULT --> AUDITW["audit_log.log()\nWrite sanitized entry\n(tier 2 or 3)"]
    AUDITW --> SUCC{"result.success?"}
    SUCC -->|"Yes"| SPEAK["server.add_loki_message()\n+ tts.speak(result.message)"]
    SUCC -->|"No"| FAIL["server.add_loki_message()\n'That operation failed…'\ntts.speak()"]
    SPEAK --> IDLE["server.set_status('idle')"]
    FAIL --> IDLE
    CHAT --> IDLE2["server.set_status('idle')"]
    IDLE --> TIMEOUT["_reset_timeout()\n30s inactivity timer\nOn expire: farewell message + hide window"]
```

---

### 4.7 Action Router — Full Intent Dispatch Map

The Action Router holds a flat dispatch table of 42 intent strings, each mapped to a handler method that calls into the registered action or feature module.

```mermaid
graph LR
    AR["ActionRouter\nroute_intent(intent)"] --> FILE["File Operations\n────────────────\nfile_create → FileOps.create_file\nfile_delete → FileOps.delete_file\nfile_move   → FileOps.move\nfile_read   → inline handler\nfolder_create → FileOps.create_folder\nfolder_delete → FileOps.delete_folder\nfile_search → FileSearch.search\nfile_organize → FileOrganizer.organize"]

    AR --> SYS["System Control\n────────────────\nvolume_set/get → SystemCtrl\nbrightness_set/get → SystemCtrl\nwifi_toggle → SystemCtrl\nbluetooth_toggle → SystemCtrl\napp_open/close → AppCtrl\nbrowser_open/search → BrowserCtrl\nsystem_monitor → SystemMonitor\nprocess_list/kill → ProcessManager"]

    AR --> SHELL["Shell\n────────────────\nshell → ShellExec.execute\n(allowlist + blocklist check)"]

    AR --> INTEL["Intelligence\n────────────────\nweb_summarize → WebSummarizer\npdf_chat → PDFChat\ncode_analyze → CodeAssistant\ncode_convert → CodeAssistant\nreadme_generate → CodeAssistant\nregex_generate → CodeAssistant\nsql_build → CodeAssistant\ngit_status → GitHelper\ngit_commit → GitHelper\ncommit_message → GitHelper\nsecurity_scan → SecurityScanner"]

    AR --> PROD["Productivity\n────────────────\nfocus_mode_enable/disable → FocusMode\ntask_add/list/complete/delete → TaskManager\nclipboard_show/clear → ClipboardManager\nvault_store/retrieve → Vault"]

    AR --> META["Meta\n────────────────\nundo → UndoStack.pop_and_undo\nchat → return intent.message as-is"]
```

---

### Action Return Contract
Every feature and action handler returns a standardised dictionary:
```python
{"success": bool, "message": str, "data": Optional[Any]}
```
`message` is always safe to speak aloud — it never contains secrets. `data` carries the full structured payload for the frontend.

---

## 5. Core Intelligence Features

### 5.1 Brain — LLM Integration

The Brain is the central reasoning engine. It receives a user utterance, constructs a structured prompt, calls the LLM, and either returns a plain text response or an intent JSON payload that the Action Router dispatches.

**LLM Priority Cascade:**
1. **Ollama** (local, preferred) — runs on `localhost:11434`, uses `phi3:mini` by default
2. **OpenRouter Primary** — cloud fallback, uses configured `fallback_model`
3. **OpenRouter Secondary** — final fallback if primary is unavailable

**Prompt construction (KORTEX-style, 5 layers):**

```mermaid
flowchart TD
    subgraph Prompt["Final LLM Prompt  (assembled top-to-bottom)"]
        L1["① System Prompt\nLoki personality · capability list · intent format spec"]
        L2["② Brain Memory\nUser facts · preferences · decisions · session summaries\n≤ 1500 token budget"]
        L3["③ RAG Context\nTop-5 doc chunks above 0.45 cosine similarity\nInjected only when relevant files are indexed"]
        L4["④ Conversation History\nLast N turns — auto-compressed at 40 messages\nOldest 20 summarised → stored back in Brain Memory"]
        L5["⑤ User Message\nCurrent utterance (voice transcript or typed text)"]
        L1 --> L2 --> L3 --> L4 --> L5
    end

    L5 --> LLM["LLM\nOllama / OpenRouter"]
    LLM --> OUT{"Response\ntype?"}
    OUT -->|"plain text"| REPLY["Text reply → TTS + chat bubble"]
    OUT -->|"intent JSON"| AR["Action Router → dispatch handler"]
```

**Automatic conversation compression:** When conversation history exceeds 40 messages, the Brain uses the LLM to summarise the oldest 20 turns into a single summary entry and stores it in brain memory. This keeps context windows manageable while preserving long-term facts.

**Fact extraction:** Every 5 user exchanges, the Brain runs a background LLM pass over recent history to extract persistent facts (user preferences, names, recurring patterns) and stores them in `brain.json`.

**Configurable parameters:**
- `max_tokens`: 400 (response length cap)
- `temperature`: 0.75 (creativity vs determinism)
- `max_turns`: 20 (history window before compression)

---

### 5.2 Brain Memory — Persistent Knowledge Store

A structured JSON store (`loki/memory/brain.json`) that survives across sessions. It is the long-term memory layer injected into every prompt.

**Data schema:**
| Field | Type | Capacity | Description |
|-------|------|----------|-------------|
| `personality` | string | — | Current mode: `loki`, `jarvis`, `friday` |
| `user_profile.name` | string | — | User's preferred name |
| `user_profile.preferences` | dict | — | Key-value preference store |
| `key_facts` | list | 50 max | Auto-extracted facts (FIFO eviction) |
| `architecture_decisions` | list | 30 max | Timestamped decisions the user has made |
| `session_summaries` | list | 20 max | Compressed conversation snapshots |

Thread safety is enforced via `threading.RLock`. All writes use a deepcopy before serialisation to prevent concurrent mutation. Failures re-raise after cleanup so callers can surface the error rather than silently losing data.

---

### 5.3 Personality Modes

Three distinct response personas, switchable at runtime via the UI or by voice:

| Mode | Character | Tone | Voice |
|------|-----------|------|-------|
| **Loki** | Norse trickster — witty, sharp, occasionally sarcastic | Playful, concise | en-GB-RyanNeural |
| **Jarvis** | Formal AI butler — precise, efficient, no-nonsense | Professional, clipped | Configurable |
| **Friday** | Collaborative assistant — warm, encouraging, conversational | Friendly, thorough | Configurable |

Switching personality persists to `brain.json` and takes effect immediately on the next response. The frontend reflects the change through a color-coded badge (gold for Loki, sky blue for Jarvis, green for Friday).

---

### 5.4 RAG Engine — Semantic Document Search

Allows users to upload files that Loki can consult when answering questions. All embedding and retrieval happen locally using Ollama's `nomic-embed-text` model.

**Supported file types:** `.py`, `.js`, `.ts`, `.tsx`, `.jsx`, `.go`, `.rs`, `.java`, `.cpp`, `.c`, `.h`, `.md`, `.txt`, `.yaml`, `.yml`, `.json`, `.toml`, `.pdf` (via PyMuPDF), `.sql`, `.sh`

**Pipeline:**

```mermaid
flowchart LR
    subgraph Ingest["📥 Ingest  (on upload)"]
        UP["POST /upload\n≤ 10 MB"] --> EXT["Text Extraction\nPlain text: direct read\nPDF: PyMuPDF fitz"]
        EXT --> CHUNK["Semantic Chunking\n400 words / chunk\n40-word overlap"]
        CHUNK --> EMBED["Ollama\nnomic-embed-text\n→ float vector"]
        EMBED --> IDX[("rag_index.json\nvector store")]
    end

    subgraph Query["🔍 Query  (on every chat turn)"]
        Q["User utterance"] --> QE["Embed query\nnomic-embed-text"]
        QE --> SIM["Cosine similarity\nvs all stored vectors"]
        SIM --> FILTER["Filter\nsimilarity ≥ 0.45"]
        FILTER --> TOP["Top-5 chunks"]
        TOP --> INJECT["Inject into\nPrompt Layer ③"]
    end

    IDX --> SIM
```

**Index format:** Lightweight JSON (no ChromaDB or vector database dependency) — runs on any machine with Python and Ollama.

---

### 5.5 Web Summarizer

Fetches any URL, strips boilerplate (navigation, footers, scripts, ads), and returns a 3–5 bullet-point summary powered by the LLM.

**Intent:** `web_summarize`  
**Parameters:** `url` (required)

**Process:**
1. HTTP GET with realistic User-Agent header, 10-second timeout
2. BeautifulSoup HTML parsing — removes `<nav>`, `<footer>`, `<script>`, `<style>`, `<header>`
3. Remaining text passed to LLM for summarisation
4. Fallback (no LLM): returns first 3 paragraphs verbatim

**Example:** *"Loki, summarise this article: https://example.com/post"*

---

### 5.6 PDF Chat

Enables conversational Q&A against any PDF document without uploading it to the RAG index.

**Intent:** `pdf_chat`  
**Parameters:** `path` (PDF file path), `question` (natural language question)

**Process:**
1. Extracts all text from the PDF using PyMuPDF (`fitz`)
2. Caches extracted text in memory for the session (avoids re-parsing repeated queries)
3. Injects full document text + question into LLM prompt
4. Returns targeted answer referencing document content

**Example:** *"Loki, read my contract.pdf and tell me what the termination clause says."*

---

## 6. File & Folder Operations

All file operations are sandboxed to the user's home directory (`~`). Any attempt to access a path outside `~` is rejected before the OS call is made.

### 6.1 File Create
**Intent:** `file_create`  
**Parameters:** `path` (relative or absolute within `~`), `content` (optional text body)

Creates a new text file. Parent directories are created automatically. If the file already exists it is overwritten. The operation is logged at audit tier 2 and pushed to the undo stack with a snapshot of the pre-existing content.

**Example:** *"Loki, create a file called notes.txt with the contents 'Meeting at 3pm tomorrow'."*

---

### 6.2 File Delete
**Intent:** `file_delete`  
**Parameters:** `path`

Reads and snapshots the file content before deletion so the undo operation can recreate it exactly. Requires user confirmation (configurable via `confirm_destructive`). Logged at audit tier 3.

**Example:** *"Loki, delete old_draft.py."*

---

### 6.3 File Move
**Intent:** `file_move`  
**Parameters:** `src`, `dst`

Moves or renames a file or folder. Detects destination conflicts and returns an error rather than silently overwriting. Original location stored for undo.

**Example:** *"Loki, move project_v1 to archive/project_v1."*

---

### 6.4 File Read
**Intent:** `file_read`  
**Parameters:** `path`

Reads a file and returns its contents. The spoken `message` field contains the first 2000 characters; the full content is available in the `data` field. UTF-8 decoding with error replacement.

**Example:** *"Loki, read my config.yaml."*

---

### 6.5 Folder Create
**Intent:** `folder_create`  
**Parameters:** `path`

Creates a directory tree (`mkdir -p` equivalent). No-op if it already exists.

---

### 6.6 Folder Delete
**Intent:** `folder_delete`  
**Parameters:** `path`

Snapshots the entire directory tree structure before deletion so undo can reconstruct all files and subdirectories. Requires confirmation. Logged at audit tier 3.

**Example:** *"Loki, delete the temp_build folder."*

---

### 6.7 File Search
**Intent:** `file_search`  
**Parameters:** `query`, `directory` (optional, defaults to `~`), `type` (optional filter: pdf, image, video, code, etc.)

Natural language file search across the filesystem with relevance scoring:

| Signal | Score Boost |
|--------|------------|
| Modified today | +5 |
| Filename matches query keyword | +3 |
| File content matches query keyword | +1.5 per match |

Supports temporal keywords: *"today"*, *"last week"*, *"last month"*. Reads file contents up to 10 MB for in-document keyword matching. Returns up to 20 results with filename, path, size, modified date, and relevance score.

**Example:** *"Loki, find PDF files about machine learning I looked at this week."*

---

### 6.8 File Organizer
**Intent:** `file_organize`  
**Parameters:** `directory` (optional, defaults to `~/Downloads`)

Automatically sorts all files in the target directory into category subfolders by extension:

| Folder | Extensions |
|--------|-----------|
| Images | .jpg .jpeg .png .gif .bmp .webp .svg .ico .tiff |
| Documents | .pdf .doc .docx .xls .xlsx .ppt .pptx .odt .rtf .txt |
| Videos | .mp4 .avi .mkv .mov .wmv .flv .webm .m4v |
| Audio | .mp3 .wav .flac .aac .ogg .m4a .wma |
| Code | .py .js .ts .tsx .jsx .go .rs .java .cpp .c .h .cs .php .rb .swift .kt |
| Archives | .zip .rar .7z .tar .gz .bz2 .xz |
| Executables | .exe .msi .bat .cmd .ps1 .sh |
| Data | .json .xml .csv .yaml .yml .toml .sql .db .sqlite |

Handles filename conflicts by appending `_1`, `_2`, etc. Logs each move at audit tier 2.

**Example:** *"Loki, organise my Downloads folder."*

---

## 7. System Control Features

### 7.1 Volume Control
**Intents:** `volume_set`, `volume_get`  
**Parameters:** `percent` (0–100 for set)

Uses the Windows Core Audio API via `pycaw`. The current volume level is read from the `IMMDeviceEnumerator` COM interface and written back via `SetMasterVolumeLevelScalar`. Volume changes are pushed to the undo stack so *"undo"* restores the previous level.

**Example:** *"Loki, set volume to 40."* / *"Loki, what's the current volume?"*

---

### 7.2 Brightness Control
**Intents:** `brightness_set`, `brightness_get`  
**Parameters:** `percent` (0–100 for set)

Uses the `screen_brightness_control` library which wraps the WMI interface on Windows. Supports multi-monitor setups. Changes pushed to undo stack.

**Example:** *"Loki, lower brightness to 30 percent."*

---

### 7.3 Wi-Fi Toggle
**Intent:** `wifi_toggle`  
**No parameters**

Enables or disables the system Wi-Fi adapter using `netsh wlan`. Detects current state and toggles accordingly. Requires admin privileges.

**Example:** *"Loki, turn off Wi-Fi."*

---

### 7.4 Bluetooth Toggle
**Intent:** `bluetooth_toggle`  
**No parameters**

Toggles the system Bluetooth radio via PowerShell and the Windows Runtime (WinRT) Bluetooth API. Detects current state before toggling.

**Example:** *"Loki, enable Bluetooth."*

---

### 7.5 Application Launch & Close
**Intents:** `app_open`, `app_close`  
**Parameters:** `name`

Built-in application map covers the most common desktop apps:

| Name | Executable / Action |
|------|-------------------|
| chrome / browser | Google Chrome |
| vs code / vscode / code | Visual Studio Code |
| discord | Discord |
| slack | Slack |
| teams | Microsoft Teams |
| spotify | Spotify |
| vlc | VLC Media Player |
| steam | Steam |
| settings | Windows Settings |
| terminal / powershell | Windows Terminal |
| notepad | Notepad |
| calculator | calc.exe |

`app_close` matches by process name or PID and sends a graceful termination signal.

**Example:** *"Loki, open VS Code."* / *"Loki, close Spotify."*

---

### 7.6 Browser Control
**Intents:** `browser_open`, `browser_search`  
**Parameters (open):** `url`  
**Parameters (search):** `query`, `engine` (optional: google, bing, duckduckgo, youtube, github)

`browser_open` validates the URL scheme (blocks `javascript://`, `data://`, `vbscript://`, `file://`) and auto-prepends `https://` if no scheme is present. Opens in the system default browser.

`browser_search` constructs the appropriate search URL for the specified engine and opens it.

**Example:** *"Loki, search YouTube for lo-fi hip hop."* / *"Loki, open github.com/torvalds/linux."*

---

### 7.7 System Monitor
**Intent:** `system_monitor`  
**No parameters**

Returns a live snapshot of system resource usage:
- CPU utilisation (percent, per-core optional)
- RAM usage (used / total / percent)
- Disk usage (used / total / percent for primary drive)
- GPU VRAM and utilisation (via `nvidia-smi`, graceful failure if no NVIDIA GPU)
- Network I/O (bytes sent / received since boot)
- Top N processes by CPU (default 10, configurable)

Alert thresholds are checked on each reading: CPU > 90% or RAM > 85% generates a warning message.

**Example:** *"Loki, how's the system doing?"*

---

### 7.8 Process Manager
**Intents:** `process_list`, `process_kill`  
**Parameters (kill):** `name_or_pid`

`process_list` returns the top 15 processes by CPU usage with PID, name, CPU%, and RAM%.

`process_kill` terminates a process by name or PID. A protected process list prevents accidental termination of system-critical processes:

> `System`, `smss.exe`, `csrss.exe`, `wininit.exe`, `winlogon.exe`, `lsass.exe`, `svchost.exe`, `explorer.exe`, `dwm.exe`, `python.exe`, `loki.exe`

Logged at audit tier 3.

**Example:** *"Loki, kill the process named node."* / *"Loki, what are the top processes right now?"*

---

### 7.9 Shell Execution
**Intent:** `shell`  
**Parameters:** `command`

Executes an arbitrary shell command subject to a two-layer safety check:

**Layer 1 — Allowlist:** The command must begin with a prefix in `data/command_allowlist.txt`. Matching is case-insensitive and prefix-based (e.g., `git` allows `git status`, `git log`, etc.).

**Layer 2 — Block patterns:** Even allowlisted commands are rejected if they match dangerous patterns:
- `rm -rf /`, `del /f /s /q c:\`, `format c:`, `mkfs`, `dd if=`, `fork bomb` patterns
- `shutdown`, `reboot`, `halt`, `poweroff`
- Any command piped to a drive-level destructive operation

Executes in a subprocess with 30-second timeout, capturing stdout + stderr. Logged at audit tier 3.

**Example:** *"Loki, run git status."* / *"Loki, run npm install."*

---

## 8. Developer Tools

### 8.1 Code Assistant
**Intents:** `code_analyze`, `code_convert`, `generate_readme`, `generate_regex`, `build_sql`

A suite of LLM-powered developer utilities:

**Code Analyze** — Reads a source file and returns a structured report covering:
- Potential bugs and logic errors
- Security vulnerabilities (injection risks, unsafe calls)
- Code smells and maintainability issues
- Suggested refactors

Supports 23 file extensions: `.py`, `.js`, `.ts`, `.tsx`, `.jsx`, `.go`, `.rs`, `.java`, `.cpp`, `.c`, `.cs`, `.rb`, `.php`, `.swift`, `.kt`, `.scala`, and more.

**Code Convert** — Translates a source file from one language to another. Preserves logic and idioms rather than doing a literal word-for-word translation. Returns the converted code as a string.

**Generate README** — Scans the specified repository path (or `./` by default), reads key files (existing README, package.json, pyproject.toml, main source files), and generates a professional README.md with: title, description, features list, installation steps, usage examples, and license section.

**Generate Regex** — Takes a plain English description and returns a tested Python-compatible regular expression pattern, with an explanation of each component.

**Build SQL** — Takes a natural language query description and an optional schema definition, returns valid SQL. Supports SELECT, INSERT, UPDATE, DELETE, JOIN, GROUP BY, window functions.

**Examples:**  
*"Loki, analyze my auth.py for security issues."*  
*"Loki, convert main.go to Python."*  
*"Loki, generate a README for this project."*  
*"Loki, write a regex that matches email addresses."*  
*"Loki, write SQL to get the top 5 customers by revenue from the orders table."*

---

### 8.2 Git Helper
**Intents:** `git_status`, `generate_commit_message`, `git_commit`

**Git Status** — Shows the current branch, number of staged files, modified files, and untracked files for any repository path.

**Generate Commit Message** — Reads `git diff --cached` (staged changes) and passes the diff to the LLM to generate a conventional commit message (max 72 characters, follows the `type(scope): description` format).

**Git Commit** — Stages all changes (`git add -A`) and commits with the provided message. Returns the commit hash.

Uses the `gitpython` library internally. Works on any local git repository.

**Examples:**  
*"Loki, what's the git status?"*  
*"Loki, generate a commit message for my changes."*  
*"Loki, commit with the message 'fix: handle null user in auth flow'."*

---

## 9. Productivity Features

### 9.1 Task Manager
**Intents:** `task_add`, `task_list`, `task_complete`, `task_delete`

A persistent priority-based task list stored in `loki/memory/tasks.json`.

**Adding a task:**
- `title` (required) — the task description
- `priority` — `critical`, `high`, `medium` (default), `low`
- `due` — optional due date string

Each task gets an auto-incremented integer ID.

**Listing tasks:**
- Default: shows only incomplete tasks, sorted by priority weight
- `filter: "all"` — includes completed tasks with completion timestamp

Priority weights for sorting: `critical=4`, `high=3`, `medium=2`, `low=1`

**Examples:**  
*"Loki, add a task to review the PR, priority high."*  
*"Loki, list my tasks."*  
*"Loki, mark task 3 as complete."*  
*"Loki, delete task 7."*

---

### 9.2 Clipboard Manager
**Intents:** `clipboard_show`, `clipboard_clear`

Monitors the system clipboard in a background thread (using `pyperclip`) and maintains a history of the last 20 copied items. Duplicate entries are moved to the front rather than stored twice.

**Show clipboard history** — Returns all 20 items with previews. Useful for recovering something copied several operations ago.

**Clear clipboard** — Wipes the entire history and the current system clipboard content.

**Example:** *"Loki, show my clipboard history."* / *"Loki, clear the clipboard."*

---

### 9.3 Focus Mode
**Intents:** `focus_mode_enable`, `focus_mode_disable`  
**Parameters (enable):** `duration_minutes` (optional)

Blocks distracting websites by adding entries to the Windows `hosts` file (`C:\Windows\System32\drivers\etc\hosts`) that redirect the sites to `127.0.0.1`.

**Default blocked sites:**
- YouTube, Reddit, Twitter, Facebook, Instagram, TikTok, Twitch, Netflix

Both the base domain and `www.` subdomain are blocked for each site. DNS cache is flushed via `ipconfig /flushdns` after each change.

If `duration_minutes` is specified, a background timer automatically re-enables internet access when the session ends.

Requires Administrator privileges. Logs at audit tier 2.

**Example:** *"Loki, enable focus mode for 90 minutes."* / *"Loki, disable focus mode."*

---

## 10. Security & Privacy Features

### 10.1 Vault — Encrypted Secret Storage
**Intents:** `vault_store`, `vault_retrieve`, `vault_list_keys`, `vault_delete`

An AES-256-GCM encrypted key-value store for passwords, API keys, and other sensitive values. All encryption and decryption happen locally.

**Cryptographic specification:**
| Parameter | Value |
|-----------|-------|
| Algorithm | AES-256-GCM (authenticated encryption) |
| Key derivation | PBKDF2-HMAC-SHA256 |
| KDF iterations | 310,000 |
| Salt | 32 bytes, random per vault |
| Nonce | 12 bytes, random per encryption |
| Auth tag | 128-bit GCM tag |

Master password is set on first use and held in memory for the session. The `message` field returned by vault operations never contains the secret value — secrets are only accessible via the `data` field. Audit logs automatically redact any parameter named `value`, `password`, `secret`, `key`, or `token`.

Atomic writes: the encrypted file is written to a `.tmp` file and then renamed, preventing partial writes from corrupting the vault.

**Examples:**  
*"Loki, store my GitHub token in the vault."*  
*"Loki, retrieve my GitHub token."*  
*"Loki, list vault keys."*  
*"Loki, delete GitHub token from the vault."*

---

### 10.2 Security Scanner
**Intent:** `security_scan`  
**Parameters:** `path` (file or directory)

Scans source code for common security vulnerabilities using 13 built-in regex patterns:

| Pattern | Detects |
|---------|---------|
| Generic API key | `api_key = "..."` hardcoded strings |
| AWS Access Key | `AKIA...` key IDs |
| Private key header | `-----BEGIN RSA PRIVATE KEY-----` |
| Password in code | `password = "..."` literals |
| Bearer token | Hardcoded Authorization headers |
| GitHub token | `ghp_` prefixed tokens |
| OpenAI key | `sk-` prefixed keys |
| Slack token | `xoxb-` prefixed tokens |
| Google API key | `AIza...` keys |
| Hardcoded IP | IP addresses in non-test code |
| SQL injection risk | String-concatenated SQL queries |
| Debug print with secrets | `print(password)` style leaks |
| Generic secret | `secret = "..."` literals |

Skips binary files and common non-source directories: `__pycache__`, `node_modules`, `.git`, `dist`, `build`, `.venv`.

Returns up to 20 findings with: filename, line number, vulnerability type, and a redacted preview of the matching line.

**Example:** *"Loki, security scan my project."*

---

### 10.3 Audit Log
A tamper-evident, append-only operation log stored as JSONL at `loki/memory/audit.jsonl`. Automatically rotates at 1000 entries.

**Three-tier classification:**

| Tier | Examples | Logged? |
|------|---------|---------|
| 1 — Safe | Chat, volume get, file search, health check | No |
| 2 — Moderate | File/folder create/move, volume set, app open/close, task ops, focus mode | Yes |
| 3 — Restricted | File delete, folder delete, process kill, shell execution, security scan | Yes, marked restricted |

Each log entry contains: timestamp (ISO 8601), intent name, sanitized parameters, success/failure, tier, and a preview of the result message.

**Automatic sanitization:** Any parameter key matching `password`, `secret`, `token`, `key`, or `value` has its value replaced with `"[REDACTED]"` before logging.

**Circular reference detection:** The sanitizer detects and breaks object cycles (replaces with `"<circular>"`) to prevent infinite serialisation loops.

**Example:** *"Loki, show the audit log."*

---

## 11. Voice Interface

### Voice Pipeline Overview

```mermaid
flowchart TD
    MIC["🎙 Microphone\nsounddevice · 16kHz mono"] --> CHUNK["2-second audio chunks"]
    CHUNK --> RMS{"RMS silence\ncheck\nthreshold 0.01"}
    RMS -->|"silent"| CHUNK
    RMS -->|"audio present"| WW{"Wakeword\nbackend?"}

    WW -->|"whisper"| WHIN["Whisper tiny.en\ntranscribe chunk"]
    WW -->|"porcupine"| PORC["Porcupine\nhot-word model\nPicoVoice key required"]

    WHIN --> MATCH{"Contains\n'Hey Loki'\nor variant?"}
    PORC --> MATCH

    MATCH -->|"No"| CHUNK
    MATCH -->|"Yes"| CHIME["🔔 Wakeword chime\n(if audio cues enabled)"]
    CHIME --> STATUS["WebSocket: status → listening"]
    STATUS --> LISTEN["Record full utterance\nuntil silence > 1.5s"]
    LISTEN --> STT["Whisper base.en\nFull transcription"]
    STT --> TRANS["WebSocket: transcript → frontend\n(live preview)"]
    TRANS --> BRAIN["Send to Brain\nfor processing"]
    BRAIN --> RESP["Text response"]
    RESP --> MUTED{"Muted?"}
    MUTED -->|"Yes"| CHAT["Chat bubble only"]
    MUTED -->|"No"| TTS

    subgraph TTS["TTS Engine"]
        direction LR
        E1["edge-tts\nen-GB-RyanNeural"] -.->|"fallback"| E2["pyttsx3\nlocal system TTS"]
    end

    TTS --> AUDIO["pygame.mixer\nPlayback"]
```

### 11.1 Wakeword Detection
Loki listens continuously in the background and activates when it hears a trigger phrase.

**Default wakeword:** *"Hey Loki"*

**Recognised variants:**
- "Hey Loki", "Hey Lolly", "Okay Loki", "Hey Lucky", "Loki" (standalone)

**Method:** Audio is captured via `sounddevice` at 16 kHz mono. Every 2-second chunk is transcribed using OpenAI Whisper (`tiny.en` model, CPU inference). RMS silence filtering (threshold 0.01) skips quiet chunks to reduce CPU load.

**Optional Porcupine backend:** If a PicoVoice access key is configured, the more accurate Porcupine hot-word model is used instead of Whisper for wakeword detection. Whisper is still used for full speech-to-text transcription.

---

### 11.2 Speech-to-Text (STT)
After wakeword activation, full utterances are transcribed using Whisper (`base.en` by default). The Whisper model is loaded once at startup and shared between wakeword detection and STT to avoid the expensive re-initialisation penalty.

Live transcript is streamed to the frontend via WebSocket `transcript` messages so the user can see what Loki is hearing in real time.

---

### 11.3 Text-to-Speech (TTS)
Loki speaks every response aloud.

**Primary engine:** `edge-tts` (Microsoft Neural Text-to-Speech)
- Default voice: `en-GB-RyanNeural` (British male, natural cadence)
- Rate and volume configurable as relative adjustments (e.g., `+10%`, `-5%`)
- Fully async — runs in a daemon thread, does not block the main event loop

**Fallback engine:** `pyttsx3` (local system TTS, no internet required)

**Audio playback:** `pygame.mixer` (primary), PowerShell `Media.SoundPlayer` (fallback)

Mute state is persisted across the current session. When muted, TTS output is suppressed but responses still appear in the chat UI.

---

## 12. Web UI

The frontend is a Next.js static export served by the FastAPI backend from `loki-ui/out/`. It communicates with the backend exclusively via WebSocket and REST endpoints on port 7777.

### 12.1 Layout

```mermaid
graph TD
    subgraph AppShell["Full-Page App Shell  100vw × 100vh"]
        BG["🎨 RuneCanvas  z=0\nAnimated Norse rune particles\nWebGL background"]
        VIG["Depth Vignette  z=1\nRadial purple + gold gradients\npointer-events: none"]

        subgraph Layer["UI Layer  z=10  flex-row"]
            subgraph Sidebar["File Sidebar  280px  flex-col\n(visible when Files toggled)"]
                SH["Header: 'File Knowledge' + close btn"]
                SDZ["Drop zone\ndrag-and-drop or click to upload"]
                SFL["File list\nfilename · chunk count · delete btn"]
                SFT["Footer: file count summary"]
                SH --> SDZ --> SFL --> SFT
            end

            subgraph Chat["Chat Area  flex-1  flex-col"]
                subgraph Header["Header  60px  app-header"]
                    LOGO["LOKI logo\ngold shimmer"]
                    PDIV["│ divider"]
                    PBTN["Personality btn\ndot · label · chevron"]
                    RAGP["RAG pill (when files indexed)"]
                    OFFB["Offline banner (when disconnected)"]
                    STAT["Status pill\nidle · listening · thinking · speaking"]
                    LOGO --> PDIV --> PBTN
                    RAGP --> OFFB --> STAT
                end

                subgraph Body["Chat Body  flex-1  overflow-y-auto"]
                    MSG["Message bubbles\nLoki left · User right · System center"]
                    THINK["Thinking indicator\n3 colored bouncing dots"]
                    TRANS["Live transcript strip\nshown during listening"]
                end

                subgraph InputBar["Input Bar  flex-shrink-0"]
                    FIELD["Text input field"]
                    SEND["Send button"]
                    ACTS["Action row:\nFiles · Mic · Undo · Clear"]
                end

                Header --> Body --> InputBar
            end
        end

        BG -.-> VIG -.-> Layer
    end

    subgraph Portal["Portal  document.body  z=9999"]
        PPICK["Personality Picker dropdown\nLoki · Jarvis · Friday\nfixed position, click-outside closes"]
    end

    PBTN -.->|"toggle"| PPICK
```

Full-page layout with three regions:
- **Header (60px):** Loki logo, personality selector, RAG indicator, offline banner, status pill
- **Main body (flex-1):** Optional file sidebar (280px) + scrollable message area
- **Input bar:** Text field, Send button, action buttons (Files, Mic, Undo, Clear)

An animated Norse rune particle canvas (`RuneCanvas`) renders in the background layer.

### 12.2 Chat Interface
- Messages rendered as animated bubbles (Framer Motion)
- Loki responses left-aligned with avatar dot; user messages right-aligned
- System notifications centered in a muted pill style
- Thinking indicator: three colored bouncing dots while Loki is processing
- Live transcript strip shown during active listening
- Auto-scrolls to newest message

### 12.3 Personality Selector
A dropdown portal (rendered into `document.body` to escape `overflow: hidden`) that lets the user switch between Loki / Jarvis / Friday modes. Shows the current personality's color-coded dot and name. Errors from failed personality changes are shown inline in the picker (not as chat messages).

Accessibility: `aria-expanded` and `aria-pressed` are set imperatively via `useEffect` + `setAttribute` (not JSX expressions) to satisfy static accessibility analyzers.

### 12.4 File Panel (RAG)
A collapsible 280px sidebar that:
- Shows all currently indexed files with chunk count
- Provides a drag-and-drop upload zone (10 MB limit per file)
- Shows per-file delete buttons
- Displays a "No embed model" warning if Ollama's embedding model is not available

### 12.5 Status Pill
A compact header pill showing Loki's current activity with animated dots:

| Status | Color | Animation |
|--------|-------|-----------|
| Idle | Slate | Static |
| Listening | Gold | Pulse |
| Thinking | Sky blue | Spin |
| Speaking | Green | Beat |
| Offline | Red | Static |

### 12.6 Undo
The Undo button (or *"Loki, undo"*) reverses the last reversible action. The undo stack is maintained in memory for the current session (max 25 entries) and supports:
- File creates → delete the created file
- File deletes → recreate with original content
- File moves → move back to original location
- Folder creates → delete the folder
- Folder deletes → recreate with original directory tree
- Volume changes → restore previous volume level
- Brightness changes → restore previous brightness level

---

## 13. API Reference

All endpoints run on `http://localhost:7777`.

### WebSocket — `/ws`
Bidirectional real-time channel. All messages are JSON.

**Client → Server:**
| Type | Fields | Description |
|------|--------|-------------|
| `user_message` | `text: string` | Send a message to Loki |
| `mute_toggle` | `muted: boolean` | Toggle TTS output |
| `undo` | — | Request an undo action |

**Server → Client:**
| Type | Fields | Description |
|------|--------|-------------|
| `status` | `status: idle\|listening\|thinking\|speaking\|offline` | Current Loki state |
| `transcript` | `text: string` | Live speech-to-text result |
| `clear_transcript` | — | Clear transcript display |
| `loki_message` | `text: string` | Loki's text response |
| `system_message` | `text: string` | System notification |
| `personality_changed` | `mode: string` | Personality switch confirmation |
| `file_indexed` | `filename: string, chunk_count: number` | File upload complete |
| `show` / `hide` | — | Window visibility control |

---

### REST Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Returns `{status, rag_available, brain_loaded}` |
| `GET` | `/files` | Lists indexed files with chunk counts |
| `POST` | `/upload` | Upload a file for RAG indexing (multipart/form-data, 10 MB limit) |
| `DELETE` | `/upload/{filename}` | Remove a file from the RAG index |
| `GET` | `/brain` | Returns full brain memory JSON |
| `POST` | `/brain/personality` | Switch personality `{mode: "loki"\|"jarvis"\|"friday"}` |
| `GET` | `/audit` | Returns recent audit entries `?limit=20&tier=2` |

---

## 14. Configuration Reference

All configuration lives in `loki/config.yaml`. Key sections:

### LLM
```yaml
llm:
  ollama_model: phi3:mini          # Local model (Ollama)
  fallback_model: openai/gpt-4o-mini   # Cloud fallback (OpenRouter)
  max_tokens: 400
  temperature: 0.75
  ollama_port: 11434
```

### Whisper (STT)
```yaml
whisper:
  model: base.en      # tiny.en is faster; large-v3 is most accurate
  device: cpu         # or cuda for GPU acceleration
  language: en
```

### TTS
```yaml
tts:
  engine: edge        # edge | pyttsx3 | luxtts
  voice: en-GB-RyanNeural
  rate: "+0%"         # relative speed adjustment
  volume: "+0%"       # relative volume adjustment
  fallback_engine: pyttsx3
```

### Wakeword
```yaml
wakeword:
  method: whisper     # whisper | porcupine
  keyword: "hey loki"
  chunk_duration: 2.0
  check_interval: 0.5
  porcupine_sensitivity: 0.5
```

### UI Server
```yaml
ui:
  port: 7777
  conversation_timeout_seconds: 30
```

### Audio
```yaml
audio:
  sample_rate: 16000
  channels: 1
  vad_aggressiveness: 2
  silence_duration: 1.5
  enable_audio_cues: true
  wakeword_chime: true
  error_sound: true
```

### Actions
```yaml
actions:
  allowlist_file: data/command_allowlist.txt
  home_dir_only: true
  shell_timeout: 30
  confirm_destructive: true
```

### Features (Sample)
```yaml
features:
  file_search:
    max_results: 20
    search_content: true
    max_file_size_mb: 10

  system_monitor:
    update_interval: 2
    alert_cpu_percent: 90
    alert_ram_percent: 85

  focus_mode:
    block_sites:
      - youtube.com
      - reddit.com
      - twitter.com
      - facebook.com
      - instagram.com
      - tiktok.com
      - twitch.tv
      - netflix.com

  vault:
    algorithm: AES-256-GCM
    pbkdf2_iterations: 310000

  undo:
    max_depth: 25
```

---

## 15. Data Persistence & Storage

```mermaid
graph LR
    subgraph Runtime["Runtime — in-memory"]
        BR["Brain\nconversation buffer\nundo stack"]
        RAG_M["RAG Engine\nvector cache"]
        CB["Clipboard Manager\n20-item ring buffer"]
    end

    subgraph Files["loki/memory/  — persisted to disk"]
        CONV["conversation.json\nLast 20 turns · JSON array"]
        BJ["brain.json\npersonality · facts · decisions\nsummaries · user profile"]
        TJ["tasks.json\nTask list with priorities"]
        VE["vault.enc\nAES-256-GCM ciphertext"]
        RI["rag_index.json\nEmbedding vectors + chunk metadata"]
        UPL["uploads/\nOriginal indexed documents"]
        AJ["audit.jsonl\nAppend-only · 1000-entry rotation"]
        LOG["loki.log\nPython logging · plain text"]
    end

    BR -->|"every exchange"| CONV
    BR -->|"every 5 exchanges\n+ personality changes"| BJ
    BR -->|"on task op"| TJ
    BR -->|"on vault write/delete"| VE
    RAG_M -->|"on file upload/delete"| RI
    RAG_M -->|"on file upload/delete"| UPL
    BR -->|"on tier 2/3 action"| AJ
    BR -->|"continuously"| LOG
```

All persistent state lives under `loki/memory/`:

| File | Format | Contents | Updated |
|------|--------|----------|---------|
| `conversation.json` | JSON array | Last 20 chat turns | Each exchange |
| `brain.json` | JSON object | Personality, facts, decisions, summaries, user profile | Every 5 exchanges (facts), on personality change, on session end |
| `tasks.json` | JSON array | Task list with priorities and completion state | On each task operation |
| `vault.enc` | Encrypted binary | AES-256-GCM ciphertext of key-value secrets | On vault write/delete |
| `rag_index.json` | JSON array | Embedding vectors + chunk metadata for uploaded files | On upload/delete |
| `uploads/` | Raw files | Original uploaded documents | On upload/delete |
| `audit.jsonl` | JSON lines | Append-only action log (1000 entry rotation) | On every tier 2/3 action |
| `loki.log` | Plain text | Python logging output | Continuously |

---

## 16. Security Constraints & Safety Model

### Security Decision Flow

Every incoming intent passes through multiple independent safety gates before any OS operation is attempted:

```mermaid
flowchart TD
    IN(["Intent + params\nfrom LLM"]) --> T1{"Tier check\nIs intent\ndestructive?"}

    T1 -->|"Tier 1 – safe\nchat, volume_get…"| EXEC
    T1 -->|"Tier 2 – moderate\nfile ops, app open…"| CONF{"confirm_destructive\nenabled?"}
    T1 -->|"Tier 3 – restricted\ndelete, shell, kill…"| CONF

    CONF -->|"No"| PATH
    CONF -->|"Yes"| ASK["Request user\nconfirmation"]
    ASK -->|"Denied"| DENY(["❌ Rejected\nreturn error"])
    ASK -->|"Approved"| PATH

    PATH{"File op?\nPath check"}
    PATH -->|"Not a file op"| SHELL
    PATH -->|"Yes"| SAND{"is_relative_to\nPath.home()?"}
    SAND -->|"Outside home dir"| DENY
    SAND -->|"Within home dir"| SHELL

    SHELL{"Shell\nexecution?"}
    SHELL -->|"No"| PROC
    SHELL -->|"Yes"| AL{"Command matches\nallowlist prefix?"}
    AL -->|"No match"| DENY
    AL -->|"Matched"| BL{"Matches blocked\npattern?\nrm -rf / · format · shutdown…"}
    BL -->|"Blocked"| DENY
    BL -->|"Clear"| PROC

    PROC{"Process\nkill?"}
    PROC -->|"No"| EXEC
    PROC -->|"Yes"| PROT{"Name in\nprotected list?\nexplorer · lsass · svchost…"}
    PROT -->|"Protected"| DENY
    PROT -->|"Safe to kill"| EXEC

    EXEC(["✅ Execute operation"])
    EXEC --> LOG{"Tier ≥ 2?"}
    LOG -->|"Yes"| AUDIT["Write sanitized entry\nto audit.jsonl\n(secrets redacted)"]
    LOG -->|"No"| UNDO
    AUDIT --> UNDO{"Reversible\naction?"}
    UNDO -->|"Yes"| STACK["Push snapshot\nto undo stack\nmax 25 entries"]
    UNDO -->|"No"| DONE(["Return result dict\n{success, message, data}"])
    STACK --> DONE
```

### Path Sandboxing
Every file path argument is validated against the user's home directory (`Path.home()`) using `is_relative_to()`. Any path that would escape `~` is rejected before touching the OS. This is enforced in `FileOps._safe()`, called by every file operation.

### Shell Safety
Shell execution requires the command to match an allowlist prefix AND pass a blocklist pattern check. There is no way to run arbitrary commands, even if the LLM generates them. The allowlist is a plain text file that administrators can modify.

### Secret Hygiene
- Vault `message` fields never contain secret values
- Audit log sanitizer redacts sensitive parameter keys before writing
- LLM prompts never include raw vault contents
- Circular reference detection in the sanitizer prevents serialisation crashes

### Protected Processes
The process kill feature maintains a hardcoded list of system-critical process names that cannot be terminated regardless of what the LLM requests.

### URL Safety
The browser open feature validates URL schemes and rejects `javascript://`, `data://`, `vbscript://`, and `file://` to prevent potential local file disclosure or script injection.

### Destructive Confirmation
File delete, folder delete, and process kill operations check `confirm_destructive: true` in config. When enabled, these require explicit user confirmation before execution.

---

## 17. Dependencies & Requirements

### System Requirements
- **OS:** Windows 10 / 11 (uses Windows-specific COM, netsh, PowerShell, WMI APIs)
- **Python:** 3.10+
- **RAM:** 4 GB minimum; 8 GB recommended (Whisper + Ollama)
- **Admin Privileges:** Required for volume control, brightness, Wi-Fi toggle, Bluetooth toggle, focus mode
- **Ollama (optional):** Provides local LLM and local embeddings — fully offline operation

### Required Python Packages
`fastapi`, `uvicorn`, `websockets`, `openai`, `requests`, `numpy`, `pydantic`

### Optional Packages (by feature)
| Package | Feature |
|---------|---------|
| `edge-tts` | Primary TTS |
| `pyttsx3` | TTS fallback |
| `pygame` | Audio playback |
| `openai-whisper` | STT + wakeword detection |
| `sounddevice` | Microphone input |
| `PyMuPDF (fitz)` | PDF text extraction |
| `gitpython` | Git helper |
| `psutil` | Process manager, system monitor |
| `screen-brightness-control` | Brightness control |
| `pycaw` | Windows volume control |
| `pyperclip` | Clipboard manager |
| `cryptography` | Vault encryption |
| `beautifulsoup4` | Web summarizer |
| `pvporcupine` | Alternative wakeword engine |

### Environment Variables
| Variable | Required | Description |
|----------|----------|-------------|
| `OPENROUTER_API_KEY` | No* | Cloud LLM fallback (*not needed if Ollama is running) |
| `PORCUPINE_ACCESS_KEY` | No | Enables Porcupine wakeword (free tier available) |

---

## 18. Extended Feature Set (v1.1)

This section documents the 25 features added in the second development phase, bringing the total capability count to 50+.

### 18.1 Writing & Text Features

#### GhostWriter (`loki/features/ghostwriter.py`)
AI-powered long-form writing assistant.

| Method | Intent | Description |
|--------|--------|-------------|
| `expand(text)` | `text_expand` | Expand a short note or bullet point into a full paragraph |
| `continue_text(text)` | `text_continue` | Continue writing from where the user left off |
| `bullets_to_prose(text)` | `text_bullets_to_prose` | Convert a bullet list into flowing prose |

#### GrammarPolisher (`loki/features/grammar_polisher.py`)
Grammar correction and tone transformation.

| Method | Intent | Description |
|--------|--------|-------------|
| `polish(text)` | `text_polish` | Fix grammar, clarity, and style issues |
| `change_tone(text, tone)` | `text_change_tone` | Rewrite in formal / casual / persuasive / academic tone |
| `translate(text, language)` | `text_translate` | Translate to any language via LLM |

#### CitationGenerator (`loki/features/citation_generator.py`)
Academic citation formatting from URLs or manual metadata.

- Supports: **APA**, **MLA**, **Chicago**, **IEEE**
- URL mode: fetches Open Graph / meta tags via requests + BeautifulSoup
- Manual mode: formats from author/title/year/publisher dict

#### EmailDrafter (`loki/features/email_drafter.py`)
Professional email and reply generation via LLM.

- `draft(subject, context, to?)` → full email body
- `reply(original, intent?)` → contextual reply

#### FactChecker (`loki/features/fact_checker.py`)
Claim verification using DuckDuckGo HTML search + LLM verdict.

```mermaid
flowchart TD
    A[Claim text] --> B[DuckDuckGo HTML search]
    B --> C[Extract top 3 result snippets]
    C --> D[LLM verdict: True/False/Unverifiable]
    D --> E[Return verdict + evidence]
```

#### DailyBriefing (`loki/features/daily_briefing.py`)
Morning brief combining: date/time, pending tasks, system health summary, top news headlines. Integrates `TaskManager`, `SystemMonitor`, and `NewsAggregator`.

---

### 18.2 Data & Conversion Features

#### CurrencyConverter (`loki/features/currency_converter.py`)
- **Live rates:** `open.er-api.com/v6/latest/{base}` (free, no key)
- **LLM fallback:** if API unreachable, asks LLM for approximate rate
- **Unit conversion:** 50+ SI units — length, mass, temperature, volume, speed, data, pressure, energy

#### NewsAggregator (`loki/features/news_aggregator.py`)
RSS-based news aggregation with no external dependencies beyond `requests`.

Topics: technology, science, world, business, sports — each mapped to a BBC/Reuters RSS feed URL.  
XML parsed via `xml.etree.ElementTree` (stdlib only).

#### MediaConverter (`loki/features/media_converter.py`)
ffmpeg subprocess wrapper for audio/video/image format conversion.

```mermaid
flowchart LR
    A[Input file] --> B{ffmpeg on PATH?}
    B -->|No| C[Return error with install URL]
    B -->|Yes| D[Quality preset mapping]
    D --> E[subprocess.run ffmpeg]
    E -->|rc=0| F[Return output path + size]
    E -->|rc!=0| G[Return stderr]
```

---

### 18.3 Software & Environment Features

#### SoftwareUpdater (`loki/features/software_updater.py`)
Windows Package Manager (winget) integration.

| Method | Intent |
|--------|--------|
| `check_updates()` | `update_check` |
| `update_all()` | `update_all` |
| `update_package(name)` | `update_package` |
| `install_package(name)` | `install_package` |

Gracefully reports if winget is not installed (Microsoft Store).

#### EnvSetup (`loki/features/env_setup.py`)
LLM-generated project environment configuration.

- Reads key project files (`requirements.txt`, `package.json`, `go.mod`, etc.) to infer stack
- Generates: production Dockerfile (multi-stage), PowerShell venv setup script, docker-compose.yml

#### ApiMocker (`loki/features/api_mocker.py`)
LLM-generated mock API server code (FastAPI) + sample JSON data.

---

### 18.4 File Management Features

#### BackupManager (`loki/features/backup_manager.py`)
Timestamped file and directory backups via `shutil`.

- Default backup root: `~/LokiBackups/`
- Directory backup skips: `__pycache__`, `node_modules`, `.git`, `.venv`, `.next`
- `list_backups(filter?)` — shows recent 20 backup entries

#### DigitalDeclutter (`loki/features/digital_declutter.py`)
Storage cleanup analysis.

```mermaid
flowchart TD
    A[suggest_cleanup] --> B[find_duplicates]
    A --> C[find_large_files]
    A --> D[find_old_files]
    B --> E[MD5 hash per file via hashlib]
    E --> F[Group by identical hash]
    C --> G[os.walk + stat.st_size filter]
    D --> H[stat.st_mtime vs cutoff date]
```

- Skips: `.git`, `node_modules`, `__pycache__`, `.venv`, `.next`, `dist`, `build`
- Reports wasted space in MB for each duplicate group

---

### 18.5 Window & Process Features

#### WindowTiler (`loki/features/window_tiler.py`)
Windows window management using ctypes (no pywin32 dependency).

**Layouts:** `left`, `right`, `top`, `bottom`, `topleft`, `topright`, `bottomleft`, `bottomright`, `maximize`, `center`

```mermaid
flowchart TD
    A[snap_window layout] --> B[_calc layout → x,y,w,h]
    B --> C{window_title given?}
    C -->|Yes| D[EnumWindows → match title]
    C -->|No| E[GetForegroundWindow]
    D --> F[MoveWindow via user32]
    E --> F
```

- `tile_all()` — enumerates visible non-minimized windows, arranges in N×M grid
- Work area from `SystemParametersInfoW(SPI_GETWORKAREA)` — respects taskbar

#### ProcessTriage (`loki/features/process_triage.py`)
Resource management for demanding applications.

- `analyze()` — top N processes by RAM, flags safe-to-close candidates
- `triage_for_app(app_name, dry_run)` — terminates non-essential processes (Discord, Slack, Steam, etc.)
- `suspend_process / resume_process` — SIGSTOP/SIGCONT equivalent via `psutil.Process.suspend()`
- Protected list: system, csrss, lsass, winlogon, explorer, dwm, and other critical processes

---

### 18.6 Security & Privacy Features

#### PhishingDetector (`loki/features/phishing_detector.py`)
Two-layer phishing analysis.

**Heuristic signals:**
- IP address as hostname instead of domain name
- Domain resembles known brand (homograph/lookalike check)
- Excessive subdomains (> 4 levels)
- Suspicious TLDs (`.tk`, `.ml`, `.xyz`, etc.)
- URL contains `@` symbol
- Sensitive keywords in path (`login`, `verify`, `secure`, etc.)
- Email: phishing language patterns, urgency words, credential requests

**LLM layer:** if heuristic risk ≥ 3, sends URL + signals to LLM for a brief verdict.

Risk scoring: 0–10. Low: 0–2 / Medium: 3–5 / High: 6–10.

#### FootprintAuditor (`loki/features/footprint_auditor.py`)
Windows privacy and persistence audit.

| Method | Intent | Data Source |
|--------|--------|-------------|
| `audit_startup()` | `footprint_startup` | Registry Run keys + Startup folders |
| `audit_scheduled_tasks()` | `footprint_tasks` | PowerShell `Get-ScheduledTask` |
| `audit_privacy_settings()` | `footprint_privacy` | Registry `CapabilityAccessManager` |
| `audit_network_listeners()` | `footprint_network` | PowerShell `Get-NetTCPConnection` |
| `full_audit()` | `footprint_full` | All four above |

Flags scheduled tasks using PowerShell, cmd, mshta, rundll32 as potentially suspicious.

---

### 18.7 Knowledge & History Features

#### KnowledgeGraph (`loki/features/knowledge_graph.py`)
Personal knowledge graph over local notes and files.

```mermaid
flowchart TD
    A[ingest_file / ingest_directory] --> B[Read file text up to 3000 chars]
    B --> C{LLM available?}
    C -->|Yes| D[LLM extracts entities + relations as JSON]
    C -->|No| E[Regex: capitalized multi-word phrases]
    D --> F[Merge into nodes and edges dicts]
    E --> F
    F --> G[Persist to ~/.loki_knowledge_graph.json]
    H[query / find_connections] --> I[Build graph summary string]
    I --> J[LLM answers from graph context]
```

- Supported file types: `.txt`, `.md`, `.rst`, `.py`, `.js`, `.ts`, `.json`, `.yaml`
- Entity types: person, place, organization, concept, technology, event, project
- `find_connections(entity)` — shows all graph edges for a node

#### SemanticBrowserHistory (`loki/features/semantic_browser_history.py`)
Search over Chrome / Edge / Brave SQLite history databases.

- Copies history DB to temp file (browsers hold a lock on the live file)
- Chromium timestamp decoding: microseconds since 1601-01-01 → UTC datetime
- `search(query)` — keyword match over title and URL
- `semantic_search(query)` — sends compact history listing to LLM, returns most relevant entries
- `get_stats()` — top 10 domains by visit count over last 30 days

---

### 18.8 Meeting Features

#### MeetingTranscriber (`loki/features/meeting_transcriber.py`)
Meeting audio transcription and minutes generation using Whisper.

```mermaid
flowchart TD
    A[generate_minutes audio_path] --> B[transcribe via Whisper]
    B --> C{Transcription OK?}
    C -->|No| D[Return error]
    C -->|Yes| E[Build minutes prompt]
    E --> F[LLM generates structured minutes]
    F --> G[Return transcript + minutes]
```

Minutes structure:
1. Meeting Summary (2–3 sentences)
2. Key Discussion Points (bullet list)
3. Decisions Made
4. Action Items (person → task)
5. Next Steps

- `extract_action_items(text_or_path)` — works on audio files, text files, or raw transcript strings
- Shares the global Whisper model instance from the STT module (no double-load)

---

### 18.9 Action Router Additions

All 25 new features are registered in `ActionRouter.route_intent()`. Total intent count: **70+**.

```mermaid
graph LR
    subgraph Writing
        W1[text_expand] --> GW[GhostWriter]
        W2[text_continue] --> GW
        W3[text_bullets_to_prose] --> GW
        W4[text_polish] --> GP[GrammarPolisher]
        W5[text_change_tone] --> GP
        W6[text_translate] --> GP
        W7[citation_from_url] --> CG[CitationGenerator]
        W8[email_draft] --> ED[EmailDrafter]
        W9[fact_check] --> FC[FactChecker]
        W10[daily_briefing] --> DB[DailyBriefing]
    end
    subgraph Data
        D1[currency_convert] --> CC[CurrencyConverter]
        D2[unit_convert] --> CC
        D3[news_headlines] --> NA[NewsAggregator]
        D4[media_convert] --> MC[MediaConverter]
        D5[update_check] --> SU[SoftwareUpdater]
    end
    subgraph Files
        F1[backup_file] --> BM[BackupManager]
        F2[backup_directory] --> BM
        F3[declutter_duplicates] --> DD[DigitalDeclutter]
        F4[env_dockerfile] --> ES[EnvSetup]
    end
    subgraph WindowProc
        P1[window_snap] --> WT[WindowTiler]
        P2[window_tile_all] --> WT
        P3[process_analyze] --> PT[ProcessTriage]
        P4[process_triage] --> PT
    end
    subgraph Security
        S1[phishing_url] --> PD[PhishingDetector]
        S2[footprint_full] --> FA[FootprintAuditor]
    end
    subgraph Knowledge
        K1[kg_ingest_file] --> KG[KnowledgeGraph]
        K2[kg_query] --> KG
        K3[history_search] --> BH[BrowserHistory]
        K4[history_semantic] --> BH
        K5[meeting_transcribe] --> MTR[MeetingTranscriber]
        K6[meeting_minutes] --> MTR
    end
```

---

*End of LokiPRD.md*
