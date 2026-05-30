---
type: community
cohesion: 0.40
members: 5
---

# _whisper_device (auto cuda/cpu reso / config: whisper.device auto / SpeechListener

**Cohesion:** 0.40 - moderately connected
**Members:** 5 nodes

## Members
- [[Rationale GPU via uvpy3.12 (no CUDA wheels for 3.14)]] - code - loki/core/listener.py
- [[SpeechListener_1]] - code - loki/core/listener.py
- [[WakewordDetector_1]] - code - loki/core/wakeword.py
- [[_whisper_device (auto cudacpu resolver)]] - code - loki/core/listener.py
- [[config whisper.device auto]] - code - loki/config.yaml

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_whisper_device_auto_cuda/cpu_reso_/_config_whisperdevice_auto_/_SpeechListener
SORT file.name ASC
```
