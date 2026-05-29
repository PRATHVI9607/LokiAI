---
type: community
cohesion: 0.11
members: 19
---

# Community 21

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
TABLE source_file, type FROM #community/Community_21
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiBrain  test_brain.py  .ask()]]

## Top bridge nodes
- [[EnvSetup_1]] - degree 2, connects to 1 community
- [[GitHelper_1]] - degree 2, connects to 1 community