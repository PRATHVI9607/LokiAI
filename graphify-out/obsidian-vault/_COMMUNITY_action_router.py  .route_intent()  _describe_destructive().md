---
type: community
cohesion: 0.50
members: 4
---

# action_router.py / .route_intent() / _describe_destructive()

**Cohesion:** 0.50 - moderately connected
**Members:** 4 nodes

## Members
- [[.route_intent()]] - code - loki/core/action_router.py
- [[Action router — maps LLM intents to featureaction handlers. Destructive operati]] - rationale - loki/core/action_router.py
- [[_describe_destructive()]] - code - loki/core/action_router.py
- [[action_router.py]] - code - loki/core/action_router.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/action_routerpy_/_route_intent_/__describe_destructive
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_ActionRouter  ._handle_agent_cancel()  ._handle_agent_status()]]
- 1 edge to [[_COMMUNITY__missing()  ._handle_agent_run()  ._handle_api_mock_data()]]

## Top bridge nodes
- [[action_router.py]] - degree 4, connects to 2 communities
- [[.route_intent()]] - degree 2, connects to 1 community