---
type: community
cohesion: 0.33
members: 6
---

# Voice Pipeline (Mic â†’ Wakeword â† / TTS Engine edge-tts (en-GB-RyanNeur / Wakeword Detection (Hey Loki varian

**Cohesion:** 0.33 - loosely connected
**Members:** 6 nodes

## Members
- [[Optional Porcupine Wakeword Backend]] - document - LokiPRD.md
- [[Speech-to-Text via Whisper base.en]] - document - LokiPRD.md
- [[TTS Engine edge-tts (en-GB-RyanNeural primary)]] - document - LokiPRD.md
- [[TTS Fallback pyttsx3 (local system TTS)]] - document - LokiPRD.md
- [[Voice Pipeline (Mic â†’ Wakeword â†’ STT â†’ Brain â†’ TTS)]] - document - LokiPRD.md
- [[Wakeword Detection (Hey Loki variants)]] - document - LokiPRD.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Voice_Pipeline_Mic__Wakeword__/_TTS_Engine_edge-tts_en-GB-RyanNeur_/_Wakeword_Detection_Hey_Loki_varian
SORT file.name ASC
```
