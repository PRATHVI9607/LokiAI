---
type: community
cohesion: 0.18
members: 12
---

# LokiBrain.ask / WebSummarizer.summarize / LokiBrain._build_system_prompt

**Cohesion:** 0.18 - loosely connected
**Members:** 12 nodes

## Members
- [[INTENT_CATALOG (system prompt intent list)]] - code - loki/core/brain.py
- [[LLM Provider Chain (Kimi K2 â†’ OpenRouter â†’ Ollama)]] - code - loki/core/brain.py
- [[LokiBrain._build_system_prompt]] - code - loki/core/brain.py
- [[LokiBrain._call_llm]] - code - loki/core/brain.py
- [[LokiBrain._compress_old_turns]] - code - loki/core/brain.py
- [[LokiBrain._extract_facts]] - code - loki/core/brain.py
- [[LokiBrain._get_kg_context]] - code - loki/core/brain.py
- [[LokiBrain._get_rag_context]] - code - loki/core/brain.py
- [[LokiBrain.ask]] - code - loki/core/brain.py
- [[WebSummarizer DNS-rebinding guard (_SSRFBlockingAdapter)]] - code - loki/features/web_summarizer.py
- [[WebSummarizer SSRF guard (_is_ssrf_risk)]] - code - loki/features/web_summarizer.py
- [[WebSummarizer.summarize]] - code - loki/features/web_summarizer.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/LokiBrainask_/_WebSummarizersummarize_/_LokiBrain_build_system_prompt
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_ActionRouter.route_intent  AutoAgent._execute_task  _DESTRUCTIVE_INTENTS Frozenset]]
- 1 edge to [[_COMMUNITY_ConversationStateMachine.on_tts_done  ConversationStateMachine._arm_timeout]]

## Top bridge nodes
- [[LokiBrain.ask]] - degree 9, connects to 2 communities
- [[INTENT_CATALOG (system prompt intent list)]] - degree 2, connects to 1 community