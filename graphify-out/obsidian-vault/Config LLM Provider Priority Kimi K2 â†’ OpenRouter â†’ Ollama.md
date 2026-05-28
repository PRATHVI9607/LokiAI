---
source_file: "loki/config.yaml"
type: "document"
community: "RAG Engine Semantic Document Search / Brain LLM Engine"
tags:
  - graphify/document
  - graphify/EXTRACTED
  - community/RAG_Engine_Semantic_Document_Search_/_Brain_LLM_Engine
---

# Config: LLM Provider Priority: Kimi K2 â†’ OpenRouter â†’ Ollama

## Connections
- [[Config Kimi K2 Primary LLM (Moonshot API)]] - `references` [EXTRACTED]
- [[Config googlegemma-2-9b-itfree (second fallback)]] - `references` [EXTRACTED]
- [[Config mistralaimistral-7b-instructfree (OpenRouter fallback)]] - `references` [EXTRACTED]
- [[Config phi3mini via Ollama (local fallback)]] - `references` [EXTRACTED]
- [[LLM Fallback Chain (Ollama â†’ OpenRouter Primary â†’ Secondary)]] - `implements` [EXTRACTED]

#graphify/document #graphify/EXTRACTED #community/RAG_Engine_Semantic_Document_Search_/_Brain_LLM_Engine