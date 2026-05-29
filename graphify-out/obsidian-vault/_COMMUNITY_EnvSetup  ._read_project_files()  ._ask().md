---
type: community
cohesion: 0.14
members: 19
---

# EnvSetup / ._read_project_files() / ._ask()

**Cohesion:** 0.14 - loosely connected
**Members:** 19 nodes

## Members
- [[.__init__()_28]] - code - loki/features/env_setup.py
- [[._ask()_5]] - code - loki/features/env_setup.py
- [[._read_project_files()]] - code - loki/features/env_setup.py
- [[.generate_docker_compose()]] - code - loki/features/env_setup.py
- [[.generate_dockerfile()]] - code - loki/features/env_setup.py
- [[.generate_venv_script()]] - code - loki/features/env_setup.py
- [[.save_docker_compose()]] - code - loki/features/env_setup.py
- [[.save_dockerfile()]] - code - loki/features/env_setup.py
- [[.save_venv_script()]] - code - loki/features/env_setup.py
- [[EnvSetup]] - code - loki/features/env_setup.py
- [[EnvSetup — generate Docker, virtual environment, and dependency configuration fo]] - rationale - loki/features/env_setup.py
- [[Generate a PowerShell venv setup script preview. Does NOT write automatically.]] - rationale - loki/features/env_setup.py
- [[Generate a docker-compose.yml preview. Does NOT write automatically.]] - rationale - loki/features/env_setup.py
- [[Generate a production-ready Dockerfile preview. Does NOT write automatically.]] - rationale - loki/features/env_setup.py
- [[Read key project files to understand the stack.]] - rationale - loki/features/env_setup.py
- [[Write a previously generated Dockerfile to disk.]] - rationale - loki/features/env_setup.py
- [[Write a previously generated docker-compose.yml to disk.]] - rationale - loki/features/env_setup.py
- [[Write a previously generated venv script to disk.]] - rationale - loki/features/env_setup.py
- [[env_setup.py]] - code - loki/features/env_setup.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/EnvSetup_/__read_project_files_/__ask
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  BrowserCtrl  DailyBriefing]]
- 1 edge to [[_COMMUNITY_LokiBrain  DailyBriefing  CodeAssistant]]

## Top bridge nodes
- [[EnvSetup]] - degree 13, connects to 3 communities