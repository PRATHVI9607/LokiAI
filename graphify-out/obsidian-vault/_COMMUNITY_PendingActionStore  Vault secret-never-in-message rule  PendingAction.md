---
type: community
cohesion: 0.50
members: 4
---

# PendingActionStore / Vault secret-never-in-message rule / PendingAction

**Cohesion:** 0.50 - moderately connected
**Members:** 4 nodes

## Members
- [[PendingAction_1]] - code - loki/core/pending_actions.py
- [[PendingActionStore_1]] - code - loki/core/pending_actions.py
- [[Vault secret-never-in-message rule]] - code - loki/features/vault.py
- [[Vault.retrieve]] - code - loki/features/vault.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/PendingActionStore_/_Vault_secret-never-in-message_rule_/_PendingAction
SORT file.name ASC
```
