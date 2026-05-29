---
type: community
cohesion: 0.17
members: 13
---

# Preview-First Pattern (pending_writ / CodeAssistant / No auto git add -A (only staged fil

**Cohesion:** 0.17 - loosely connected
**Members:** 13 nodes

## Members
- [[CodeAssistant_1]] - code - loki/features/code_assistant.py
- [[EnvSetup_1]] - code - loki/features/env_setup.py
- [[EnvSetup.generate_docker_compose]] - code - loki/features/env_setup.py
- [[EnvSetup.generate_dockerfile]] - code - loki/features/env_setup.py
- [[EnvSetup.generate_venv_script]] - code - loki/features/env_setup.py
- [[EnvSetup.save_docker_compose]] - code - loki/features/env_setup.py
- [[EnvSetup.save_dockerfile]] - code - loki/features/env_setup.py
- [[EnvSetup.save_venv_script]] - code - loki/features/env_setup.py
- [[GitHelper_1]] - code - loki/features/git_helper.py
- [[GitHelper.commit]] - code - loki/features/git_helper.py
- [[GitHelper.generate_commit_message]] - code - loki/features/git_helper.py
- [[No auto git add -A (only staged files committed)]] - concept - loki/features/git_helper.py
- [[Preview-First Pattern (pending_write flag, no auto-write)]] - concept - loki/features/env_setup.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Preview-First_Pattern_pending_writ_/_CodeAssistant_/_No_auto_git_add_-A_only_staged_fil
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiBrain  DailyBriefing  .__init__()]]
- 1 edge to [[_COMMUNITY_WatchJob (polling thread, snapshot   No -y Flag (auto unique filename on  FileWatcher.watch_media_inbox]]

## Top bridge nodes
- [[Preview-First Pattern (pending_write flag, no auto-write)]] - degree 6, connects to 1 community
- [[CodeAssistant_1]] - degree 3, connects to 1 community