---
type: community
cohesion: 0.12
members: 17
---

# Wakeword Detection (Hey Loki variants)

**Cohesion:** 0.12 - loosely connected
**Members:** 17 nodes

## Members
- [[Config RMS threshold=0.006 (lowered from 0.01 to catch soft speech)]] - document - loki/config.yaml
- [[MeetingTranscriber Feature (Whisper + minutes)]] - document - LokiPRD.md
- [[Optional Porcupine Wakeword Backend]] - document - LokiPRD.md
- [[Rationale RMS Threshold Lowered to 0.006 (was 0.01, missed soft speech)]] - document - loki/config.yaml
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
TABLE source_file, type FROM #community/Wakeword_Detection_Hey_Loki_variants
SORT file.name ASC
```
