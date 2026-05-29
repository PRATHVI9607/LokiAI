---
type: community
cohesion: 0.28
members: 9
---

# RagEngine / LokiServer (FastAPI) / POST /upload RAG File Endpoint (10M

**Cohesion:** 0.28 - loosely connected
**Members:** 9 nodes

## Members
- [[ChromaDB PersistentClient]] - code - loki/features/rag_engine.py
- [[HNSW Cosine Index (loki_rag collection)]] - code - loki/features/rag_engine.py
- [[LokiServer (FastAPI)]] - code - loki/ui/server.py
- [[POST upload RAG File Endpoint (10MB cap)]] - code - loki/ui/server.py
- [[RagEngine_1]] - code - loki/features/rag_engine.py
- [[Text Chunk Pipeline (400w40w overlap)]] - code - loki/features/rag_engine.py
- [[WebSocket ws Endpoint]] - code - loki/ui/server.py
- [[WebSocket ConnectionManager]] - code - loki/ui/server.py
- [[nomic-embed-text Embedding Model]] - code - loki/features/rag_engine.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/RagEngine_/_LokiServer_FastAPI_/_POST_/upload_RAG_File_Endpoint_10M
SORT file.name ASC
```
