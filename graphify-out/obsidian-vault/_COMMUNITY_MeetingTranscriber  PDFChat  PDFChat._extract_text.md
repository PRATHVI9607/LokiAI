---
type: community
cohesion: 0.33
members: 6
---

# MeetingTranscriber / PDFChat / PDFChat._extract_text

**Cohesion:** 0.33 - loosely connected
**Members:** 6 nodes

## Members
- [[(text, page_count) Tuple Cache]] - concept - loki/features/pdf_chat.py
- [[MeetingTranscriber_1]] - code - loki/features/meeting_transcriber.py
- [[PDFChat_1]] - code - loki/features/pdf_chat.py
- [[PDFChat._extract_text]] - code - loki/features/pdf_chat.py
- [[PDFChat.ask]] - code - loki/features/pdf_chat.py
- [[Whisper Model (shared)]] - code - loki/features/meeting_transcriber.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/MeetingTranscriber_/_PDFChat_/_PDFChat_extract_text
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiBrain  DailyBriefing  CodeAssistant]]

## Top bridge nodes
- [[MeetingTranscriber_1]] - degree 3, connects to 1 community