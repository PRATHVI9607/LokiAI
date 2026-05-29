---
type: community
cohesion: 0.21
members: 12
---

# ApiMocker / .generate_mock() / ._ask()

**Cohesion:** 0.21 - loosely connected
**Members:** 12 nodes

## Members
- [[.__init__()_16]] - code - loki/features/api_mocker.py
- [[._ask()]] - code - loki/features/api_mocker.py
- [[._strip_fences()]] - code - loki/features/api_mocker.py
- [[.generate_mock()]] - code - loki/features/api_mocker.py
- [[.generate_mock_data()]] - code - loki/features/api_mocker.py
- [[.save_mock()]] - code - loki/features/api_mocker.py
- [[ApiMocker]] - code - loki/features/api_mocker.py
- [[ApiMocker — generate mock REST API server code from a plain-English description.]] - rationale - loki/features/api_mocker.py
- [[Generate a mock API server preview. Does NOT write automatically.]] - rationale - loki/features/api_mocker.py
- [[Generate mock JSON data matching a schema description.]] - rationale - loki/features/api_mocker.py
- [[Write a previously generated mock API to the home directory.]] - rationale - loki/features/api_mocker.py
- [[api_mocker.py]] - code - loki/features/api_mocker.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ApiMocker_/_generate_mock_/__ask
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  BrowserCtrl  DailyBriefing]]
- 1 edge to [[_COMMUNITY_LokiBrain  DailyBriefing  CodeAssistant]]

## Top bridge nodes
- [[ApiMocker]] - degree 10, connects to 3 communities