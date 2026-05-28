---
type: community
cohesion: 0.23
members: 13
---

# EnvSetup / ._read_project_files() / ._ask()

**Cohesion:** 0.23 - loosely connected
**Members:** 13 nodes

## Members
- [[.__init__()_25]] - code - loki/features/env_setup.py
- [[._ask()_5]] - code - loki/features/env_setup.py
- [[._read_project_files()]] - code - loki/features/env_setup.py
- [[.generate_docker_compose()]] - code - loki/features/env_setup.py
- [[.generate_dockerfile()]] - code - loki/features/env_setup.py
- [[.generate_venv_script()]] - code - loki/features/env_setup.py
- [[EnvSetup]] - code - loki/features/env_setup.py
- [[EnvSetup — generate Docker, virtual environment, and dependency configuration fo]] - rationale - loki/features/env_setup.py
- [[Generate a docker-compose.yml for a multi-service project.]] - rationale - loki/features/env_setup.py
- [[Generate a production-ready Dockerfile for a project.]] - rationale - loki/features/env_setup.py
- [[Generate a shell script to set up a Python virtual environment.]] - rationale - loki/features/env_setup.py
- [[Read key project files to understand the stack.]] - rationale - loki/features/env_setup.py
- [[env_setup.py]] - code - loki/features/env_setup.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/EnvSetup_/__read_project_files_/__ask
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  main.py]]
- 1 edge to [[_COMMUNITY_ConversationManager  .process_input()  ._speak()]]
- 1 edge to [[_COMMUNITY_LokiBrain  ApiMocker  FactChecker]]

## Top bridge nodes
- [[EnvSetup]] - degree 11, connects to 3 communities