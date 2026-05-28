---
type: community
cohesion: 0.07
members: 43
---

# LokiApplication / ActionRouter / LokiBrain

**Cohesion:** 0.07 - loosely connected
**Members:** 43 nodes

## Members
- [[APP_MAP Application Name Registry]] - code - loki/actions/app_ctrl.py
- [[ActionRouter_1]] - code - loki/core/action_router.py
- [[ApiMocker_1]] - code - loki/features/api_mocker.py
- [[AppCtrl_1]] - code - loki/actions/app_ctrl.py
- [[AuditLog_1]] - code - loki/core/audit.py
- [[BLOCKED_PATTERNS Shell Deny List]] - code - loki/actions/shell_exec.py
- [[BLOCKED_SCHEMES Security List]] - code - loki/actions/browser_ctrl.py
- [[BackupManager_1]] - code - loki/features/backup_manager.py
- [[BrainMemory_1]] - code - loki/core/brain_memory.py
- [[BrowserCtrl_1]] - code - loki/actions/browser_ctrl.py
- [[ConversationManager_1]] - code - main.py
- [[FileOps_1]] - code - loki/actions/file_ops.py
- [[FileOps._safe() Path Validation]] - code - loki/actions/file_ops.py
- [[INTENT_CATALOG LLM Prompt]] - code - loki/core/brain.py
- [[INTENT_TIERS Security Classification]] - code - loki/core/audit.py
- [[Kimi K2 LLM Provider]] - code - loki/core/brain.py
- [[LokiApplication_1]] - code - main.py
- [[LokiBrain_1]] - code - loki/core/brain.py
- [[LokiTTS_1]] - code - loki/core/tts.py
- [[METACHAR_RE Injection Guard]] - code - loki/actions/shell_exec.py
- [[MemoryManager_1]] - code - loki/core/memory.py
- [[Ollama Local LLM Provider]] - code - loki/core/brain.py
- [[OpenRouter LLM Provider]] - code - loki/core/brain.py
- [[PERSONALITY_PROMPTS Dictionary]] - code - loki/core/brain_memory.py
- [[Porcupine Wakeword Detection]] - code - loki/core/wakeword.py
- [[SEARCH_ENGINES Registry]] - code - loki/actions/browser_ctrl.py
- [[ShellExec_1]] - code - loki/actions/shell_exec.py
- [[SpeechListener_1]] - code - loki/core/listener.py
- [[SystemCtrl_1]] - code - loki/actions/system_ctrl.py
- [[UndoEntry Dataclass]] - code - loki/core/undo_stack.py
- [[UndoStack_1]] - code - loki/core/undo_stack.py
- [[WakewordDetector_1]] - code - loki/core/wakeword.py
- [[WebRTC VAD Integration]] - code - loki/core/listener.py
- [[Whisper STT Integration]] - code - loki/core/listener.py
- [[Whisper Wakeword Detection]] - code - loki/core/wakeword.py
- [[audit.jsonl Append-Only Log]] - code - loki/memory/audit.jsonl
- [[brain.json Persistent State]] - code - loki/memory/brain.json
- [[command_allowlist.txt]] - code - loki/data/command_allowlist.txt
- [[conversation.json Chat History]] - code - loki/memory/conversation.json
- [[edge-tts Provider]] - code - loki/core/tts.py
- [[pyttsx3 Fallback TTS Provider]] - code - loki/core/tts.py
- [[tasks.json]] - code - loki/memory/tasks.json
- [[user_profile.json]] - code - loki/memory/user_profile.json

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/LokiApplication_/_ActionRouter_/_LokiBrain
SORT file.name ASC
```
