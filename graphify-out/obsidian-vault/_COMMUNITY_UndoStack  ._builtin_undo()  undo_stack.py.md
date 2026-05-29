---
type: community
cohesion: 0.18
members: 14
---

# UndoStack / ._builtin_undo() / undo_stack.py

**Cohesion:** 0.18 - loosely connected
**Members:** 14 nodes

## Members
- [[.__init__()_13]] - code - loki/core/undo_stack.py
- [[.__len__()]] - code - loki/core/undo_stack.py
- [[._builtin_undo()]] - code - loki/core/undo_stack.py
- [[._restore_tree()]] - code - loki/core/undo_stack.py
- [[.clear()]] - code - loki/core/undo_stack.py
- [[.is_empty()]] - code - loki/core/undo_stack.py
- [[.peek()]] - code - loki/core/undo_stack.py
- [[.pop_and_undo()]] - code - loki/core/undo_stack.py
- [[.push()_1]] - code - loki/core/undo_stack.py
- [[LIFO undo stack with per-type rollback logic.]] - rationale - loki/core/undo_stack.py
- [[Undo stack — reversible action history with 25-action depth.]] - rationale - loki/core/undo_stack.py
- [[UndoEntry]] - code - loki/core/undo_stack.py
- [[UndoStack]] - code - loki/core/undo_stack.py
- [[undo_stack.py]] - code - loki/core/undo_stack.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/UndoStack_/__builtin_undo_/_undo_stackpy
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  DailyBriefing  .generate()]]

## Top bridge nodes
- [[UndoStack]] - degree 13, connects to 2 communities