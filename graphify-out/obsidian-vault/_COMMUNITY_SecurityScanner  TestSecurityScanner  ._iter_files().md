---
type: community
cohesion: 0.23
members: 13
---

# SecurityScanner / TestSecurityScanner / ._iter_files()

**Cohesion:** 0.23 - loosely connected
**Members:** 13 nodes

## Members
- [[.__init__()_43]] - code - loki/features/security_scanner.py
- [[._iter_files()]] - code - loki/features/security_scanner.py
- [[._os_walk()]] - code - loki/features/security_scanner.py
- [[._scan_file()]] - code - loki/features/security_scanner.py
- [[.scan()]] - code - loki/features/security_scanner.py
- [[.test_clean_file_no_findings()]] - code - loki/tests/test_features.py
- [[.test_detects_aws_key()]] - code - loki/tests/test_features.py
- [[.test_detects_openai_key()]] - code - loki/tests/test_features.py
- [[Scan code files for secrets and security vulnerabilities.]] - rationale - loki/features/security_scanner.py
- [[Security scanner — detect API keys, secrets, and vulnerabilities in code.]] - rationale - loki/features/security_scanner.py
- [[SecurityScanner]] - code - loki/features/security_scanner.py
- [[TestSecurityScanner]] - code - loki/tests/test_features.py
- [[security_scanner.py]] - code - loki/features/security_scanner.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/SecurityScanner_/_TestSecurityScanner_/__iter_files
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  main.py]]
- 2 edges to [[_COMMUNITY_ClipboardManager  TestClipboardManager  ._add()]]
- 2 edges to [[_COMMUNITY_FileOrganizer  TestFileOrganizer  file_organizer.py]]
- 2 edges to [[_COMMUNITY_TestTaskManager  test_features.py  memory_mgr()]]
- 2 edges to [[_COMMUNITY_Vault  TestVault  ._save()]]
- 1 edge to [[_COMMUNITY_ConversationManager  .process_input()  ._speak()]]
- 1 edge to [[_COMMUNITY_MemoryManager  ._save_json()  .add_task()]]
- 1 edge to [[_COMMUNITY_TaskManager  .ai_prioritize()  .list_tasks()]]

## Top bridge nodes
- [[SecurityScanner]] - degree 18, connects to 6 communities
- [[TestSecurityScanner]] - degree 10, connects to 6 communities