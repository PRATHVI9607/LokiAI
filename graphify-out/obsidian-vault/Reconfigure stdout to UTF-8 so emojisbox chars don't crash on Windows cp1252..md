---
source_file: "loki/core/log_setup.py"
type: "rationale"
community: "log_setup.py / setup_logging() / TerminalFormatter"
location: "L63"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/log_setuppy_/_setup_logging_/_TerminalFormatter
---

# Reconfigure stdout to UTF-8 so emojis/box chars don't crash on Windows cp1252.

## Connections
- [[_force_utf8_stdout()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/log_setuppy_/_setup_logging_/_TerminalFormatter