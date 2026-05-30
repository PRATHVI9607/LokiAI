---
type: community
cohesion: 0.15
members: 16
---

# log_setup.py / setup_logging() / TerminalFormatter

**Cohesion:** 0.15 - loosely connected
**Members:** 16 nodes

## Members
- [[.__init__()_12]] - code - loki/core/log_setup.py
- [[.format()]] - code - loki/core/log_setup.py
- [[C]] - code - loki/core/log_setup.py
- [[Compact, aligned, color-coded one-line format for the terminal.]] - rationale - loki/core/log_setup.py
- [[Configure root logger with a clean terminal handler + detailed file handler.]] - rationale - loki/core/log_setup.py
- [[Log a voice-pipeline flow transition with a visual arrow marker.     Use for the]] - rationale - loki/core/log_setup.py
- [[Loki logging — clean, color-coded terminal output with organized component tags.]] - rationale - loki/core/log_setup.py
- [[Print a boxed section banner directly to the terminal (bypasses logging).]] - rationale - loki/core/log_setup.py
- [[Reconfigure stdout to UTF-8 so emojisbox chars don't crash on Windows cp1252.]] - rationale - loki/core/log_setup.py
- [[TerminalFormatter]] - code - loki/core/log_setup.py
- [[_force_utf8_stdout()]] - code - loki/core/log_setup.py
- [[_supports_color()]] - code - loki/core/log_setup.py
- [[banner()]] - code - loki/core/log_setup.py
- [[flow()]] - code - loki/core/log_setup.py
- [[log_setup.py]] - code - loki/core/log_setup.py
- [[setup_logging()]] - code - loki/core/log_setup.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/log_setuppy_/_setup_logging_/_TerminalFormatter
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiApplication  ._init_all()  .__init__()]]

## Top bridge nodes
- [[setup_logging()]] - degree 5, connects to 1 community