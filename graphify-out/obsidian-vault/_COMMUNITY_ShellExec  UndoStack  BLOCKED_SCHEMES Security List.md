---
type: community
cohesion: 0.18
members: 12
---

# ShellExec / UndoStack / BLOCKED_SCHEMES Security List

**Cohesion:** 0.18 - loosely connected
**Members:** 12 nodes

## Members
- [[BLOCKED_PATTERNS Shell Deny List]] - code - loki/actions/shell_exec.py
- [[BLOCKED_SCHEMES Security List]] - code - loki/actions/browser_ctrl.py
- [[BrowserCtrl_1]] - code - loki/actions/browser_ctrl.py
- [[FileOps_1]] - code - loki/actions/file_ops.py
- [[FileOps._safe() Path Validation]] - code - loki/actions/file_ops.py
- [[METACHAR_RE Injection Guard]] - code - loki/actions/shell_exec.py
- [[SEARCH_ENGINES Registry]] - code - loki/actions/browser_ctrl.py
- [[ShellExec_1]] - code - loki/actions/shell_exec.py
- [[SystemCtrl_1]] - code - loki/actions/system_ctrl.py
- [[UndoEntry Dataclass]] - code - loki/core/undo_stack.py
- [[UndoStack_1]] - code - loki/core/undo_stack.py
- [[command_allowlist.txt]] - code - loki/data/command_allowlist.txt

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ShellExec_/_UndoStack_/_BLOCKED_SCHEMES_Security_List
SORT file.name ASC
```
