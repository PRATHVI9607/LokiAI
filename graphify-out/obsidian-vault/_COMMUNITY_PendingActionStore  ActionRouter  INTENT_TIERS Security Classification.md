---
type: community
cohesion: 0.29
members: 7
---

# PendingActionStore / ActionRouter / INTENT_TIERS Security Classification

**Cohesion:** 0.29 - loosely connected
**Members:** 7 nodes

## Members
- [[ActionRouter_1]] - code - loki/core/action_router.py
- [[AuditLog_1]] - code - loki/core/audit.py
- [[INTENT_TIERS Security Classification]] - code - loki/core/audit.py
- [[PendingAction_1]] - code - loki/core/pending_actions.py
- [[PendingActionStore_1]] - code - loki/core/pending_actions.py
- [[Vault secret-never-in-message rule]] - code - loki/features/vault.py
- [[Vault.retrieve]] - code - loki/features/vault.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/PendingActionStore_/_ActionRouter_/_INTENT_TIERS_Security_Classification
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiApplication._init_all  LokiApplication._wire_callbacks  ConversationStateMachine]]
- 1 edge to [[_COMMUNITY_ActionRouter.route_intent  AutoAgent._execute_task  _DESTRUCTIVE_INTENTS Frozenset]]

## Top bridge nodes
- [[PendingActionStore_1]] - degree 4, connects to 1 community
- [[ActionRouter_1]] - degree 3, connects to 1 community