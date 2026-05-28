---
type: community
cohesion: 0.16
members: 19
---

# Vault / TestVault / ._save()

**Cohesion:** 0.16 - loosely connected
**Members:** 19 nodes

## Members
- [[.__init__()_48]] - code - loki/features/vault.py
- [[._derive_key()]] - code - loki/features/vault.py
- [[._save()_1]] - code - loki/features/vault.py
- [[.delete()_1]] - code - loki/features/vault.py
- [[.list_keys()]] - code - loki/features/vault.py
- [[.retrieve()]] - code - loki/features/vault.py
- [[.store()]] - code - loki/features/vault.py
- [[.test_get_missing_key()]] - code - loki/tests/test_features.py
- [[.test_list_and_delete_keys()]] - code - loki/tests/test_features.py
- [[.test_locked_vault_rejects_ops()]] - code - loki/tests/test_features.py
- [[.test_set_and_get()]] - code - loki/tests/test_features.py
- [[.test_wrong_password_fails()]] - code - loki/tests/test_features.py
- [[.unlock()]] - code - loki/features/vault.py
- [[AES-256-GCM encrypted key-value vault.]] - rationale - loki/features/vault.py
- [[Encrypted vault — AES-256-GCM encrypted key-value storage. Master password set o]] - rationale - loki/features/vault.py
- [[TestVault]] - code - loki/tests/test_features.py
- [[Vault]] - code - loki/features/vault.py
- [[is_locked()]] - code - loki/features/vault.py
- [[vault.py]] - code - loki/features/vault.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Vault_/_TestVault_/__save
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  main.py]]
- 2 edges to [[_COMMUNITY_ClipboardManager  TestClipboardManager  ._add()]]
- 2 edges to [[_COMMUNITY_FileOrganizer  TestFileOrganizer  file_organizer.py]]
- 2 edges to [[_COMMUNITY_SecurityScanner  TestSecurityScanner  ._iter_files()]]
- 2 edges to [[_COMMUNITY_TestTaskManager  test_features.py  memory_mgr()]]
- 1 edge to [[_COMMUNITY_ConversationManager  .process_input()  ._speak()]]
- 1 edge to [[_COMMUNITY_MemoryManager  ._save_json()  .add_task()]]
- 1 edge to [[_COMMUNITY_TaskManager  .ai_prioritize()  .list_tasks()]]

## Top bridge nodes
- [[Vault]] - degree 23, connects to 6 communities
- [[TestVault]] - degree 12, connects to 6 communities