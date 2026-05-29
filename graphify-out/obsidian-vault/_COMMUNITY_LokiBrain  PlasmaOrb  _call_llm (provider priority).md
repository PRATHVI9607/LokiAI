---
type: community
cohesion: 0.08
members: 32
---

# LokiBrain / PlasmaOrb / _call_llm (provider priority)

**Cohesion:** 0.08 - loosely connected
**Members:** 32 nodes

## Members
- [[Bloom post-processing]] - code - loki-ui/components/PlasmaOrb.tsx
- [[ConversationStateMachine_1]] - code - loki/core/conversation_sm.py
- [[Custom GLSL Shader (simplex noise + fresnel)]] - code - loki-ui/components/PlasmaOrb.tsx
- [[EnergyRings]] - code - loki-ui/components/PlasmaOrb.tsx
- [[Home page (page.tsx)]] - code - loki-ui/app/page.tsx
- [[LokiBrain_1]] - code - loki/core/brain.py
- [[LokiServer (FastAPI)]] - code - loki/ui/server.py
- [[NVIDIA NIM Kimi K2.6 (fail-fast 18s)]] - code - loki/core/brain.py
- [[Orb (shader mesh)]] - code - loki-ui/components/PlasmaOrb.tsx
- [[POST upload RAG File Endpoint (10MB cap)]] - code - loki/ui/server.py
- [[ParticleField]] - code - loki-ui/components/PlasmaOrb.tsx
- [[PlasmaOrb_1]] - code - loki-ui/components/PlasmaOrb.tsx
- [[RagEngine_1]] - code - loki/features/rag_engine.py
- [[RagEngine.query]] - code - loki/features/rag_engine.py
- [[STATE_PARAMS (voice-state â†’ shader uniforms)]] - code - loki-ui/components/PlasmaOrb.tsx
- [[TerminalFormatter (color-coded tags)]] - code - loki/core/log_setup.py
- [[WebSocket ws Endpoint]] - code - loki/ui/server.py
- [[WebSocket ConnectionManager]] - code - loki/ui/server.py
- [[_NOISY_LOGGERS suppression]] - code - loki/core/log_setup.py
- [[_call_llm (provider priority)]] - code - loki/core/brain.py
- [[_call_ollama]] - code - loki/core/brain.py
- [[_embed_batch (32call batch embeddings)]] - code - loki/features/rag_engine.py
- [[_force_utf8_stdout]] - code - loki/core/log_setup.py
- [[_handle_intent (route-first then speak)]] - code - loki/core/conversation_sm.py
- [[_history_lock (thread safety)]] - code - loki/core/brain.py
- [[_process_worker]] - code - loki/core/conversation_sm.py
- [[_run_maintenance (background memory thread)]] - code - loki/core/brain.py
- [[_warmup_ollama]] - code - loki/core/brain.py
- [[index_file]] - code - loki/features/rag_engine.py
- [[parse_intent (balanced-brace extraction)]] - code - loki/core/brain.py
- [[prefer_local (Ollama-first)]] - code - loki/core/brain.py
- [[setup_logging]] - code - loki/core/log_setup.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/LokiBrain_/_PlasmaOrb_/__call_llm_provider_priority
SORT file.name ASC
```
