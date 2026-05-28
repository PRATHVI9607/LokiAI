---
type: community
cohesion: 0.13
members: 20
---

# GitHelper / GhostWriter / ._ask()

**Cohesion:** 0.13 - loosely connected
**Members:** 20 nodes

## Members
- [[.__init__()_33]] - code - loki/features/ghostwriter.py
- [[.__init__()_34]] - code - loki/features/git_helper.py
- [[._ask()_7]] - code - loki/features/ghostwriter.py
- [[._get_repo()]] - code - loki/features/git_helper.py
- [[.bullets_to_prose()]] - code - loki/features/ghostwriter.py
- [[.commit()]] - code - loki/features/git_helper.py
- [[.continue_text()]] - code - loki/features/ghostwriter.py
- [[.expand()]] - code - loki/features/ghostwriter.py
- [[.generate_commit_message()]] - code - loki/features/git_helper.py
- [[.get_status()]] - code - loki/features/git_helper.py
- [[Continue a piece of writing, matching its style and tone.]] - rationale - loki/features/ghostwriter.py
- [[Convert a bullet-point list into flowing paragraphs.]] - rationale - loki/features/ghostwriter.py
- [[Expand rough notes or bullet points into full polished prose.]] - rationale - loki/features/ghostwriter.py
- [[GhostWriter]] - code - loki/features/ghostwriter.py
- [[GhostWriter — expand notes, continue text, convert bullets to prose.]] - rationale - loki/features/ghostwriter.py
- [[Git helper — status, diff, commit message generation, commit execution.]] - rationale - loki/features/git_helper.py
- [[Git operations with LLM-powered commit message generation.]] - rationale - loki/features/git_helper.py
- [[GitHelper]] - code - loki/features/git_helper.py
- [[ghostwriter.py]] - code - loki/features/ghostwriter.py
- [[git_helper.py]] - code - loki/features/git_helper.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/GitHelper_/_GhostWriter_/__ask
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_LokiApplication  ._init_all()  main.py]]
- 2 edges to [[_COMMUNITY_ConversationManager  .process_input()  ._speak()]]
- 2 edges to [[_COMMUNITY_LokiBrain  ApiMocker  FactChecker]]

## Top bridge nodes
- [[GitHelper]] - degree 11, connects to 3 communities
- [[GhostWriter]] - degree 10, connects to 3 communities