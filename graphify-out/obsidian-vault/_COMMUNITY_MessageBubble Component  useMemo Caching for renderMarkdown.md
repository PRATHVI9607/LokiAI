---
type: community
cohesion: 0.32
members: 8
---

# MessageBubble Component / useMemo Caching for renderMarkdown

**Cohesion:** 0.32 - loosely connected
**Members:** 8 nodes

## Members
- [[(text, page_count) Tuple Cache]] - concept - loki/features/pdf_chat.py
- [[MessageBubble Component]] - code - loki-ui/components/MessageBubble.tsx
- [[PDFChat_1]] - code - loki/features/pdf_chat.py
- [[PDFChat._extract_text]] - code - loki/features/pdf_chat.py
- [[PDFChat.ask]] - code - loki/features/pdf_chat.py
- [[inlineRender (lightweight inline markdown, no external dep)]] - code - loki-ui/components/MessageBubble.tsx
- [[renderMarkdown (block-level fenced code, lists, paragraphs)]] - code - loki-ui/components/MessageBubble.tsx
- [[useMemo Caching for renderMarkdown]] - concept - loki-ui/components/MessageBubble.tsx

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/MessageBubble_Component_/_useMemo_Caching_for_renderMarkdown
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiBrain  test_brain.py  .ask()]]

## Top bridge nodes
- [[PDFChat_1]] - degree 2, connects to 1 community