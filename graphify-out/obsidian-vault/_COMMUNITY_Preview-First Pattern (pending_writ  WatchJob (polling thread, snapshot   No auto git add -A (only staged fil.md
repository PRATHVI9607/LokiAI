---
type: community
cohesion: 0.11
members: 19
---

# Preview-First Pattern (pending_writ / WatchJob (polling thread, snapshot  / No auto git add -A (only staged fil

**Cohesion:** 0.11 - loosely connected
**Members:** 19 nodes

## Members
- [[EnvSetup_1]] - code - loki/features/env_setup.py
- [[EnvSetup.generate_docker_compose]] - code - loki/features/env_setup.py
- [[EnvSetup.generate_dockerfile]] - code - loki/features/env_setup.py
- [[EnvSetup.generate_venv_script]] - code - loki/features/env_setup.py
- [[EnvSetup.save_docker_compose]] - code - loki/features/env_setup.py
- [[EnvSetup.save_dockerfile]] - code - loki/features/env_setup.py
- [[EnvSetup.save_venv_script]] - code - loki/features/env_setup.py
- [[FileWatcher_1]] - code - loki/features/file_watcher.py
- [[FileWatcher.watch_for_backup]] - code - loki/features/file_watcher.py
- [[FileWatcher.watch_media_inbox]] - code - loki/features/file_watcher.py
- [[GitHelper_1]] - code - loki/features/git_helper.py
- [[GitHelper.commit]] - code - loki/features/git_helper.py
- [[GitHelper.generate_commit_message]] - code - loki/features/git_helper.py
- [[MediaConverter_1]] - code - loki/features/media_converter.py
- [[MediaConverter.convert]] - code - loki/features/media_converter.py
- [[No -y Flag (auto unique filename on collision)]] - concept - loki/features/media_converter.py
- [[No auto git add -A (only staged files committed)]] - concept - loki/features/git_helper.py
- [[Preview-First Pattern (pending_write flag, no auto-write)]] - concept - loki/features/env_setup.py
- [[WatchJob (polling thread, snapshot diff)]] - code - loki/features/file_watcher.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Preview-First_Pattern_pending_writ_/_WatchJob_polling_thread_snapshot__/_No_auto_git_add_-A_only_staged_fil
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiBrain  DailyBriefing  CodeAssistant]]

## Top bridge nodes
- [[EnvSetup_1]] - degree 2, connects to 1 community
- [[GitHelper_1]] - degree 2, connects to 1 community