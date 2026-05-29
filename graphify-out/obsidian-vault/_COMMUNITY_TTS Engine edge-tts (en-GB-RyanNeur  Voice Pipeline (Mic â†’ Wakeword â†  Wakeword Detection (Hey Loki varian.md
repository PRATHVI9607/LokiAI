---
type: community
cohesion: 0.14
members: 15
---

# TTS Engine edge-tts (en-GB-RyanNeur / Voice Pipeline (Mic â†’ Wakeword â† / Wakeword Detection (Hey Loki varian

**Cohesion:** 0.14 - loosely connected
**Members:** 15 nodes

## Members
- [[MeetingTranscriber Feature (Whisper + minutes)]] - document - LokiPRD.md
- [[Optional Porcupine Wakeword Backend]] - document - LokiPRD.md
- [[Requirement edge-tts=6.1.9 (Primary TTS)]] - document - loki/requirements.txt
- [[Requirement openai-whisper=20231117 (STT + wakeword)]] - document - loki/requirements.txt
- [[Requirement pyttsx3=2.90 (TTS fallback)]] - document - loki/requirements.txt
- [[Requirement sounddevice=0.4.6 (Microphone input)]] - document - loki/requirements.txt
- [[Requirement torch=2.1.0 + numpy=1.24.0 (WhisperML dependency)]] - document - loki/requirements.txt
- [[Speech-to-Text via Whisper base.en]] - document - LokiPRD.md
- [[TTS Engine edge-tts (en-GB-RyanNeural primary)]] - document - LokiPRD.md
- [[TTS Fallback pyttsx3 (local system TTS)]] - document - LokiPRD.md
- [[Tech Stack OpenAI Whisper STT]] - document - README.md
- [[Tech Stack edge-tts Microsoft Neural TTS]] - document - README.md
- [[Voice Pipeline (Mic â†’ Wakeword â†’ STT â†’ Brain â†’ TTS)]] - document - LokiPRD.md
- [[Wake Word Hey Loki]] - document - README.md
- [[Wakeword Detection (Hey Loki variants)]] - document - LokiPRD.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/TTS_Engine_edge-tts_en-GB-RyanNeur_/_Voice_Pipeline_Mic__Wakeword__/_Wakeword_Detection_Hey_Loki_varian
SORT file.name ASC
```
