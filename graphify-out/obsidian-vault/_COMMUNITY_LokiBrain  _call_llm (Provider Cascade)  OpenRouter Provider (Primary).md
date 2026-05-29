---
type: community
cohesion: 0.10
members: 29
---

# LokiBrain / _call_llm (Provider Cascade) / OpenRouter Provider (Primary)

**Cohesion:** 0.10 - loosely connected
**Members:** 29 nodes

## Members
- [[COM Thread Requirement Fix (pyttsx3 Windows)]] - code - loki/core/tts.py
- [[ConversationStateMachine_1]] - code - main.py
- [[Fast Models List (_fast_models)]] - code - loki/core/brain.py
- [[GPT-OSS-120B Benchmarked Speed ~10s]] - document - loki/config.yaml
- [[Gemma 4-31B Benchmarked Speed ~5.6s]] - document - loki/config.yaml
- [[Kimi Moonshot Provider (Tertiary)]] - code - loki/core/brain.py
- [[Liquid LFM-2.5 Benchmarked Speed ~1.1s (emergency)]] - document - loki/config.yaml
- [[LokiApplication_1]] - code - main.py
- [[LokiBrain_1]] - code - loki/core/brain.py
- [[LokiTTS_1]] - code - loki/core/tts.py
- [[NVIDIA NIM Provider (Deep Reasoning Secondary)]] - code - loki/core/brain.py
- [[Ollama Local Provider (Offline Fallback)]] - code - loki/core/brain.py
- [[OpenRouter 30s Timeout (Reduced from 60s)]] - code - loki/core/brain.py
- [[OpenRouter Provider (Primary)]] - code - loki/core/brain.py
- [[Provider Priority Comment in config.yaml]] - document - loki/config.yaml
- [[Queue Drain on stop() â€” No Premature Mic Return]] - code - loki/core/tts.py
- [[Speed-First Provider Architecture]] - code - loki/core/brain.py
- [[Thinking Mode Latency Concern (30-90s)]] - code - loki/core/brain.py
- [[VoicePipeline_1]] - code - main.py
- [[_call_llm (Provider Cascade)]] - code - loki/core/brain.py
- [[_queue_worker (TTS Serialization Thread)]] - code - loki/core/tts.py
- [[_wire_callbacks (Thin Event Wiring)]] - code - main.py
- [[fallback_model openaigpt-oss-120bfree]] - document - loki/config.yaml
- [[fast_model googlegemma-4-31b-itfree]] - document - loki/config.yaml
- [[is_idle Property]] - code - loki/core/tts.py
- [[nvidia_thinking Config Flag]] - code - loki/core/brain.py
- [[nvidia_thinking false (speed over depth)]] - document - loki/config.yaml
- [[pythoncom.CoInitialize() in Worker Thread]] - code - loki/core/tts.py
- [[second_fallback_model liquidlfm-2.5-1.2b-instructfree]] - document - loki/config.yaml

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/LokiBrain_/__call_llm_Provider_Cascade_/_OpenRouter_Provider_Primary
SORT file.name ASC
```
