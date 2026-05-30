---
type: community
cohesion: 0.12
members: 23
---

# KnowledgeGraph / .ingest_file() / ._extract_entities()

**Cohesion:** 0.12 - loosely connected
**Members:** 23 nodes

## Members
- [[.__init__()_42]] - code - loki/features/knowledge_graph.py
- [[._extract_entities()]] - code - loki/features/knowledge_graph.py
- [[._llm()_2]] - code - loki/features/knowledge_graph.py
- [[._load()_1]] - code - loki/features/knowledge_graph.py
- [[._save()]] - code - loki/features/knowledge_graph.py
- [[.clear()_2]] - code - loki/features/knowledge_graph.py
- [[.find_connections()]] - code - loki/features/knowledge_graph.py
- [[.get_stats()]] - code - loki/features/knowledge_graph.py
- [[.ingest_directory()]] - code - loki/features/knowledge_graph.py
- [[.ingest_file()]] - code - loki/features/knowledge_graph.py
- [[.query()]] - code - loki/features/knowledge_graph.py
- [[.query_entities()]] - code - loki/features/knowledge_graph.py
- [[Answer a question about the knowledge graph via LLM.]] - rationale - loki/features/knowledge_graph.py
- [[Fast entity lookup for RAG context fusion — no LLM needed.         Uses word-bou]] - rationale - loki/features/knowledge_graph.py
- [[Find all nodes connected to an entity.]] - rationale - loki/features/knowledge_graph.py
- [[Ingest all supported files in a directory.]] - rationale - loki/features/knowledge_graph.py
- [[KnowledgeGraph]] - code - loki/features/knowledge_graph.py
- [[KnowledgeGraph — extract entities and relationships from notesfiles, build a si]] - rationale - loki/features/knowledge_graph.py
- [[Read a file and add its entities to the graph.]] - rationale - loki/features/knowledge_graph.py
- [[Return graph statistics.]] - rationale - loki/features/knowledge_graph.py
- [[Use LLM to extract entities and relationships from text.]] - rationale - loki/features/knowledge_graph.py
- [[_word_boundary_match()]] - code - loki/features/knowledge_graph.py
- [[knowledge_graph.py]] - code - loki/features/knowledge_graph.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/KnowledgeGraph_/_ingest_file_/__extract_entities
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  .__init__()]]
- 1 edge to [[_COMMUNITY_LokiBrain  DailyBriefing  CodeAssistant]]

## Top bridge nodes
- [[KnowledgeGraph]] - degree 16, connects to 2 communities