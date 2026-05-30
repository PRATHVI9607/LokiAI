---
type: community
cohesion: 0.32
members: 8
---

# RagEngine / LokiServer (FastAPI) / _embed_batch (32/call batch embeddi

**Cohesion:** 0.32 - loosely connected
**Members:** 8 nodes

## Members
- [[LokiServer (FastAPI)]] - code - loki/ui/server.py
- [[POST upload RAG File Endpoint (10MB cap)]] - code - loki/ui/server.py
- [[RagEngine_1]] - code - loki/features/rag_engine.py
- [[RagEngine.query]] - code - loki/features/rag_engine.py
- [[WebSocket ws Endpoint]] - code - loki/ui/server.py
- [[WebSocket ConnectionManager]] - code - loki/ui/server.py
- [[_embed_batch (32call batch embeddings)]] - code - loki/features/rag_engine.py
- [[index_file]] - code - loki/features/rag_engine.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/RagEngine_/_LokiServer_FastAPI_/__embed_batch_32/call_batch_embeddi
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiBrain  LokiBrain._fast_intent (determinist  TerminalFormatter (color-coded tags]]

## Top bridge nodes
- [[RagEngine_1]] - degree 4, connects to 1 community