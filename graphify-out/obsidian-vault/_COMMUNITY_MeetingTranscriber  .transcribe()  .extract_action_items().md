---
type: community
cohesion: 0.21
members: 14
---

# MeetingTranscriber / .transcribe() / .extract_action_items()

**Cohesion:** 0.21 - loosely connected
**Members:** 14 nodes

## Members
- [[.__init__()_41]] - code - loki/features/meeting_transcriber.py
- [[._ensure_model()]] - code - loki/features/meeting_transcriber.py
- [[._llm()_3]] - code - loki/features/meeting_transcriber.py
- [[.extract_action_items()]] - code - loki/features/meeting_transcriber.py
- [[.generate_minutes()]] - code - loki/features/meeting_transcriber.py
- [[.summarize_transcript()]] - code - loki/features/meeting_transcriber.py
- [[.transcribe()]] - code - loki/features/meeting_transcriber.py
- [[Extract action items from transcript text or a file.]] - rationale - loki/features/meeting_transcriber.py
- [[MeetingTranscriber]] - code - loki/features/meeting_transcriber.py
- [[MeetingTranscriber — transcribe meeting audio files and generate structured minu]] - rationale - loki/features/meeting_transcriber.py
- [[Summarize a raw transcript string.]] - rationale - loki/features/meeting_transcriber.py
- [[Transcribe an audio file and return the full transcript.]] - rationale - loki/features/meeting_transcriber.py
- [[Transcribe audio and generate structured meeting minutes.]] - rationale - loki/features/meeting_transcriber.py
- [[meeting_transcriber.py]] - code - loki/features/meeting_transcriber.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/MeetingTranscriber_/_transcribe_/_extract_action_items
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  DailyBriefing  .generate()]]
- 1 edge to [[_COMMUNITY_LokiBrain  test_brain.py  .ask()]]

## Top bridge nodes
- [[MeetingTranscriber]] - degree 11, connects to 3 communities