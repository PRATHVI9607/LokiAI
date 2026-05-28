---
type: community
cohesion: 0.28
members: 9
---

# EmailDrafter / ._ask() / .draft()

**Cohesion:** 0.28 - loosely connected
**Members:** 9 nodes

## Members
- [[.__init__()_24]] - code - loki/features/email_drafter.py
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
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  main.py]]
- 1 edge to [[_COMMUNITY_ConversationManager  .process_input()  ._speak()]]
- 1 edge to [[_COMMUNITY_LokiBrain  ApiMocker  FactChecker]]

## Top bridge nodes
- [[EmailDrafter]] - degree 9, connects to 3 communities