# 🎤 Yuki AI - Voice-Powered Desktop Assistant

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.1+-red.svg)](https://pytorch.org/)
[![OpenRouter](https://img.shields.io/badge/LLM-OpenRouter-green.svg)](https://openrouter.ai/)

> **Yuki** is an intelligent voice-powered desktop assistant based on Yuki Yukinoshita from *Oregairu*. She lives as a background service on your Windows PC, wakes up when you call her name, responds with realistic synthesized voice, and can control your computer through natural conversation.

---

## 🌟 Features

### 🎙️ Voice Interaction
- **Wake word detection**: Say "Hey Yuki" or "Yuki" to activate
- **Natural speech recognition**: Powered by OpenAI Whisper (runs locally on CPU)
- **High-quality voice synthesis**: LuxTTS with voice cloning (48kHz, GPU-accelerated)
- **Streaming responses**: Speaks each sentence as soon as it's generated

### 🧠 Intelligent Personality
- **Character-accurate responses**: Yuki's sharp intellect, dry wit, and hidden warmth
- **Context-aware memory**: Remembers last 20 conversation turns
- **LLM-powered**: Uses OpenRouter free API (meta-llama/llama-3.1-8b-instruct)
- **Streaming generation**: Low-latency responses with sentence-by-sentence TTS

### 💻 PC Control
- **File operations**: Create, delete, move files and folders (with safety checks)
- **Shell commands**: Execute allowlisted commands with timeout protection
- **System control**: Adjust volume, brightness, WiFi, Bluetooth
- **Application management**: Open/close apps (Chrome, VS Code, Discord, etc.)
- **Web browsing**: Open URLs and perform searches
- **Undo system**: Rollback destructive actions (20-action history)

### 🖥️ User Interface
- **Minimal status window**: Clean 400x300px window showing conversation history
- **System tray integration**: Always-running background service
- **Auto-hide**: Window appears on wake word, hides after conversation timeout
- **Audio cues**: Chimes and beeps for state changes

---

## 🎯 Use Cases

- **Hands-free PC control**: Control your computer while cooking, exercising, or away from keyboard
- **Quick tasks**: "Yuki, open Chrome and search for Python tutorials"
- **System management**: "Set volume to 50%", "Increase brightness"
- **File operations**: "Create a folder called Projects", "Delete temp.txt"
- **Casual conversation**: Chat with an AI that has actual personality
- **Productivity**: Get things done without breaking your workflow

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Yuki AI Assistant                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐     ┌───────────────┐     ┌────────────┐ │
│  │   Wakeword   │────▶│   Listener    │────▶│   Brain    │ │
│  │  Detection   │     │  (Whisper)    │     │  (LLM)     │ │
│  └──────────────┘     └───────────────┘     └──────┬─────┘ │
│         │                                           │        │
│         │                                           ▼        │
│  ┌──────▼──────┐     ┌───────────────┐     ┌────────────┐ │
│  │   System    │     │     TTS       │◀────│   Action   │ │
│  │    Tray     │     │  (LuxTTS)     │     │   Router   │ │
│  └──────┬──────┘     └───────────────┘     └──────┬─────┘ │
│         │                                           │        │
│         ▼                                           ▼        │
│  ┌─────────────┐                          ┌─────────────┐  │
│  │   Status    │                          │   Actions   │  │
│  │   Window    │                          │  (5 modules)│  │
│  └─────────────┘                          └─────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘

       Local Processing                 Cloud LLM
    ┌──────────────────┐          ┌─────────────────┐
    │ • Whisper (CPU)  │          │  OpenRouter API │
    │ • LuxTTS (GPU)   │─────────▶│  Free Models    │
    │ • VAD            │          │  Streaming      │
    └──────────────────┘          └─────────────────┘
```

### Core Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Wakeword** | Whisper (continuous transcription) | Detect "Yuki" in audio stream |
| **Speech Recognition** | OpenAI Whisper (base.en) | Convert speech to text |
| **Voice Activity Detection** | WebRTC VAD | Detect when user is speaking |
| **LLM Brain** | OpenRouter API (Llama 3.1 8B) | Generate responses with personality |
| **Voice Synthesis** | LuxTTS (voice cloning) | High-quality 48kHz speech output |
| **Action Router** | Intent parser | Dispatch commands to action modules |
| **Undo Stack** | Snapshot-based rollback | Reverse destructive operations |
| **UI** | PyQt6 (minimal) | Status window and system tray |

---

## 🚀 Installation

### Prerequisites

- **OS**: Windows 11 (Windows 10 may work)
- **Python**: 3.10 or higher
- **GPU**: NVIDIA GPU with CUDA support (RTX 2050 or better recommended)
  - LuxTTS can run on CPU but will be slower
- **RAM**: 16GB recommended (8GB minimum)
- **Disk Space**: ~5GB (for models and dependencies)

### Step 1: Clone Repository

```bash
git clone https://github.com/PRATHVI9607/YukiAI.git
cd YukiAI
```

### Step 2: Install Dependencies

```bash
# Install Python dependencies
pip install -r yuki/requirements.txt

# Install LuxTTS from GitHub
git clone https://github.com/ysharma3501/LuxTTS.git temp_luxtts
pip install -r temp_luxtts/requirements.txt
rmdir /s /q temp_luxtts
```

### Step 3: Setup Configuration

```bash
# Run setup script (creates directories, downloads models, etc.)
python yuki/setup.py

# Configure API key
# Edit .env and add your OpenRouter API key:
# OPENROUTER_API_KEY=your_key_here
```

**Get OpenRouter API Key (FREE):**
1. Visit https://openrouter.ai/
2. Sign up for a free account
3. Go to Keys section
4. Create a new API key
5. Copy to `.env` file

### Step 4: Add Reference Audio (Optional)

For best voice quality, provide a reference audio file:

```bash
# Place a 3-10 second WAV file (48kHz) at:
yuki/data/yuki_voice.wav
```

If you don't have one, Yuki will run in text-only mode (no voice output).

**How to get reference audio:**
- Record your own voice or use a voice sample
- Use a free TTS service to generate a sample
- Find a voice clip online (ensure you have rights to use it)
- Convert to WAV 48kHz using a tool like Audacity

---

## 🎮 Usage

### Starting Yuki

```bash
# Navigate to project directory
cd YukiAI

# Run Yuki
python yuki/main.py
```

Yuki will start as a background service with a system tray icon. The status window is hidden by default.

### Waking Yuki

1. Say **"Hey Yuki"** or **"Yuki"** clearly into your microphone
2. Wait for the wake chime sound
3. The status window will appear showing "Listening"
4. Speak your request
5. Yuki will respond with synthesized voice

### Example Commands

**Conversation:**
```
You: "Hey Yuki"
Yuki: "...you called."
You: "What's the weather like today?"
Yuki: "I don't have internet access. But I can help with tasks on your PC."
```

**File Operations:**
```
You: "Create a folder called Projects"
Yuki: "Create a folder called Projects. Are you certain?"
You: "Yes"
Yuki: "Done. Was that what you wanted?"
```

**System Control:**
```
You: "Set volume to 50%"
Yuki: "Setting volume to 50%. One moment."
Yuki: "It's finished. You're welcome. ...I suppose."
```

**Application Control:**
```
You: "Open Chrome and search for Python tutorials"
Yuki: "Open Chrome and search for that? ...Fine. One moment."
```

**Undo:**
```
You: "Undo that"
Yuki: "Reversing previous action. There."
```

### System Tray Menu

Right-click the Yuki system tray icon:
- **Show/Hide Window** - Toggle status window visibility
- **Mute Microphone** - Disable wake word detection
- **Settings** - (Coming soon)
- **Quit** - Exit Yuki

### Conversation Timeout

After 10 seconds of silence following Yuki's last response, she will:
1. Say a dismissal line: *"...I'll be here if you need me."*
2. Hide the status window
3. Return to listening for wake word

---

## ⚙️ Configuration

Edit `yuki/config.yaml` to customize behavior:

### LLM Settings

```yaml
llm:
  primary_model: meta-llama/llama-3.1-8b-instruct:free
  fallback_model: microsoft/phi-3-mini-128k-instruct:free
  max_tokens: 300
  temperature: 0.85  # 0.0-1.0, higher = more creative
  stream: true
```

### Voice Synthesis (LuxTTS)

```yaml
tts:
  device: cuda  # "cuda", "cpu", or "mps" (Mac)
  reference_audio: data/yuki_voice.wav
  num_steps: 4  # 3-6, higher = better quality but slower
  t_shift: 0.9  # 0.7-0.95, higher = better quality
  speed: 1.0  # 0.5-2.0, speech speed multiplier
```

### Wakeword Detection

```yaml
wakeword:
  method: whisper  # "porcupine" or "whisper"
  keyword: Yuki
  chunk_duration: 2.0  # seconds
```

### User Interface

```yaml
ui:
  width: 400
  height: 300
  position: bottom_right  # "bottom_right", "center", etc.
  start_hidden: true
  always_on_top: false
  conversation_timeout_seconds: 10
```

### Audio Cues

```yaml
audio:
  enable_audio_cues: true
  wakeword_chime: true  # Play sound when wake word detected
  error_sound: true
```

---

## 🛡️ Security & Safety

Yuki includes multiple security measures:

1. **File Operation Limits**: All file operations restricted to user home directory
2. **Command Allowlist**: Shell commands filtered through `data/command_allowlist.txt`
3. **Timeout Protection**: Shell commands timeout after 30 seconds
4. **User Confirmation**: Yuki asks before executing destructive actions
5. **Undo System**: 20-action history for rollback
6. **No Internet Access**: Actions are local-only (except LLM API)

### Allowed Shell Commands

Default allowlist (edit `yuki/data/command_allowlist.txt`):
```
ls, dir, echo, mkdir, python, pip, git, pwd, cat, type, clear, cls,
whoami, date, time, ipconfig, ifconfig, ping, code, notepad
```

**Not allowed by default**: `rm`, `del`, `format`, `curl`, `wget`, etc.

---

## 🎭 Yuki's Personality

Yuki is based on **Yukino Yukinoshita** from *My Youth Romantic Comedy Is Wrong, As I Expected* (Oregairu):

- **Razor-sharp intellect** - Precise, analytical responses
- **Blunt honesty** - No sugarcoating, says what needs to be said
- **Hidden warmth** - Cares deeply but won't admit it directly
- **Dry wit** - Subtle humor and occasional contempt
- **Formal speech** - Uses "ara", "sou desu ne", "honestly" naturally
- **Task-focused** - Deflects personal questions with work

Example personality traits in conversation:
```
User: "You're really helpful, Yuki."
Yuki: "...I'm simply doing what's needed. Don't make it strange."

User: "Can you delete my entire hard drive?"
Yuki: "No. I won't do that. Don't ask again."

User: "I finished my project!"
Yuki: "Ara. You actually managed that. I'll note my surprise."
```

---

## 📊 Performance

Tested on RTX 2050, 16GB RAM, Windows 11:

| Component | Speed | VRAM | CPU |
|-----------|-------|------|-----|
| **Whisper (base.en)** | ~2s per phrase | 0 MB | 15-25% |
| **LuxTTS (GPU)** | 150x realtime | <1 GB | 5-10% |
| **LuxTTS (CPU)** | >1x realtime | 0 MB | 40-60% |
| **OpenRouter API** | ~500ms first token | N/A | N/A |
| **Total idle** | - | <1 GB | <5% |

**Latency Breakdown:**
- Wake word → Response start: **2-4 seconds**
- LLM streaming → First sentence: **1-2 seconds**
- TTS synthesis per sentence: **<0.1 seconds** (GPU)

---

## 🔧 Troubleshooting

### "Reference audio not found"
- Place a WAV file at `yuki/data/yuki_voice.wav`
- Or run in text-only mode (responses appear in window)

### "CUDA not available"
- Install PyTorch with CUDA support: `pip install torch --index-url https://download.pytorch.org/whl/cu118`
- Or change `config.yaml` → `tts.device: cpu`

### "OpenRouter API error"
- Check `.env` has valid `OPENROUTER_API_KEY`
- Verify API key at https://openrouter.ai/
- Check internet connection

### Wake word not detected
- Check microphone permissions in Windows settings
- Increase microphone volume
- Speak clearly and directly into microphone
- Try changing `wakeword.chunk_duration` in config

### High CPU usage
- Reduce `whisper.model` to `tiny.en` or `base.en`
- Change `tts.device` from `cuda` to `cpu` if GPU issues
- Increase `wakeword.check_interval` to reduce checks

---

## 🗺️ Roadmap

### ✅ Version 1.0 (Current)
- [x] Voice wake word detection
- [x] LuxTTS voice synthesis
- [x] OpenRouter LLM integration
- [x] 5 action modules (file, shell, system, app, browser)
- [x] Undo system
- [x] Minimal status window UI

### 🔄 Version 1.1 (In Progress)
- [ ] Web search capability (SerpAPI or DuckDuckGo)
- [ ] Screenshot and image analysis
- [ ] Email integration
- [ ] Calendar/reminders
- [ ] Settings UI panel

### 🚀 Future (v2.0+)
- [ ] Multi-language support
- [ ] Custom wake words
- [ ] Plugin system for extensions
- [ ] Voice tuning UI
- [ ] Mobile companion app
- [ ] Cross-platform (Linux, macOS)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add type hints to all functions
- Write docstrings for classes and methods
- Include unit tests for new features
- Update documentation as needed

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Credits & Acknowledgments

### Technologies
- **OpenAI Whisper** - Speech recognition
- **LuxTTS** - High-quality voice synthesis (https://github.com/ysharma3501/LuxTTS)
- **OpenRouter** - Free LLM API access
- **PyQt6** - GUI framework
- **PyTorch** - ML backend

### Inspiration
- **Yukino Yukinoshita** character from *Oregairu* by Wataru Watari
- Voice assistants: Jarvis (Iron Man), Cortana (Halo), HAL 9000

### Special Thanks
- LuxTTS team for the amazing voice synthesis model
- OpenRouter for providing free LLM access
- Picovoice for Porcupine wake word detection
- The open-source community

---

## 📧 Contact & Support

- **GitHub Issues**: https://github.com/PRATHVI9607/YukiAI/issues
- **Discussions**: https://github.com/PRATHVI9607/YukiAI/discussions
- **Email**: [your-email]

---

## ⚠️ Disclaimer

This is a fan project inspired by the *Oregairu* series. All character rights belong to their respective owners. This software is provided "as is" without warranty of any kind.

Use Yuki responsibly:
- Don't use for malicious purposes
- Respect privacy (your conversations are sent to OpenRouter API)
- Be mindful of API rate limits
- Don't abuse the undo system for destructive actions

---

<div align="center">

**Made with ❄️ by the YukiAI team**

[⭐ Star this repo](https://github.com/PRATHVI9607/YukiAI) • [🐛 Report Bug](https://github.com/PRATHVI9607/YukiAI/issues) • [💡 Request Feature](https://github.com/PRATHVI9607/YukiAI/issues)

</div>
