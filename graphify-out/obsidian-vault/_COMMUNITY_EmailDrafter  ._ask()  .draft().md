---
type: community
cohesion: 0.28
members: 9
---

# EmailDrafter / ._ask() / .draft()

**Cohesion:** 0.28 - loosely connected
**Members:** 9 nodes

## Members
- [[.__init__()_27]] - code - loki/features/email_drafter.py
- [[._ask()_4]] - code - loki/features/email_drafter.py
- [[.draft()]] - code - loki/features/email_drafter.py
- [[.reply()]] - code - loki/features/email_drafter.py
- [[Draft a new email from a description of what to say.]] - rationale - loki/features/email_drafter.py
- [[Draft a reply to an existing email thread.]] - rationale - loki/features/email_drafter.py
- [[EmailDrafter]] - code - loki/features/email_drafter.py
- [[EmailDrafter — compose and reply to emails using LLM in the user's voice. Does n]] - rationale - loki/features/email_drafter.py
- [[email_drafter.py]] - code - loki/features/email_drafter.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/EmailDrafter_/__ask_/_draft
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  DailyBriefing  .generate()]]
- 1 edge to [[_COMMUNITY_LokiBrain  test_brain.py  .ask()]]

## Top bridge nodes
- [[EmailDrafter]] - degree 8, connects to 3 communities