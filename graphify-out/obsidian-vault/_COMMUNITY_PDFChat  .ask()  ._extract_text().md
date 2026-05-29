---
type: community
cohesion: 0.33
members: 7
---

# PDFChat / .ask() / ._extract_text()

**Cohesion:** 0.33 - loosely connected
**Members:** 7 nodes

## Members
- [[.__init__()_42]] - code - loki/features/pdf_chat.py
- [[._extract_text()]] - code - loki/features/pdf_chat.py
- [[.ask()_1]] - code - loki/features/pdf_chat.py
- [[Chat with PDF documents using LLM.]] - rationale - loki/features/pdf_chat.py
- [[PDF chat — extract text from PDF and answer questions via LLM.]] - rationale - loki/features/pdf_chat.py
- [[PDFChat]] - code - loki/features/pdf_chat.py
- [[pdf_chat.py]] - code - loki/features/pdf_chat.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/PDFChat_/_ask_/__extract_text
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  DailyBriefing  .generate()]]
- 1 edge to [[_COMMUNITY_LokiBrain  test_brain.py  .ask()]]

## Top bridge nodes
- [[PDFChat]] - degree 8, connects to 3 communities