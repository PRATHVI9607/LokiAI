---
source_file: "loki/actions/file_ops.py"
type: "rationale"
community: "FileOps / ShellExec / TestFileOps"
location: "L26"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/FileOps_/_ShellExec_/_TestFileOps
---

# Returns (is_safe, resolved_path). Prevents path traversal outside trusted roots.

## Connections
- [[._safe()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/FileOps_/_ShellExec_/_TestFileOps