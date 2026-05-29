---
type: community
cohesion: 0.23
members: 13
---

# SecurityScanner / TestSecurityScanner / ._iter_files()

**Cohesion:** 0.23 - loosely connected
**Members:** 13 nodes

## Members
- [[.__init__()_46]] - code - loki/features/security_scanner.py
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
- 2 edges to [[_COMMUNITY_ClipboardManager  TestClipboardManager  ._add()]]
- 2 edges to [[_COMMUNITY_FileOrganizer  TestFileOrganizer  ._organizer()]]
- 2 edges to [[_COMMUNITY_TestTaskManager  test_features.py  memory_mgr()]]
- 2 edges to [[_COMMUNITY_Vault  TestVault  ._save()]]
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  BrowserCtrl  DailyBriefing]]
- 1 edge to [[_COMMUNITY_MemoryManager  ._save_json()  .add_task()]]
- 1 edge to [[_COMMUNITY_TaskManager  .get_memory_context()  .ai_prioritize()]]

## Top bridge nodes
- [[SecurityScanner]] - degree 17, connects to 6 communities
- [[TestSecurityScanner]] - degree 10, connects to 6 communities