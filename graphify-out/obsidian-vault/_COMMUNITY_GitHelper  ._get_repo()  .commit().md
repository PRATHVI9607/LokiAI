---
type: community
cohesion: 0.31
members: 9
---

# GitHelper / ._get_repo() / .commit()

**Cohesion:** 0.31 - loosely connected
**Members:** 9 nodes

## Members
- [[.__init__()_37]] - code - loki/features/git_helper.py
- [[._get_repo()]] - code - loki/features/git_helper.py
- [[.commit()]] - code - loki/features/git_helper.py
- [[.generate_commit_message()]] - code - loki/features/git_helper.py
- [[.get_status()]] - code - loki/features/git_helper.py
- [[Git helper — status, diff, commit message generation, commit execution.]] - rationale - loki/features/git_helper.py
- [[Git operations with LLM-powered commit message generation.]] - rationale - loki/features/git_helper.py
- [[GitHelper]] - code - loki/features/git_helper.py
- [[git_helper.py]] - code - loki/features/git_helper.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/GitHelper_/__get_repo_/_commit
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  BrowserCtrl  DailyBriefing]]
- 1 edge to [[_COMMUNITY_LokiBrain  DailyBriefing  CodeAssistant]]

## Top bridge nodes
- [[GitHelper]] - degree 10, connects to 3 communities