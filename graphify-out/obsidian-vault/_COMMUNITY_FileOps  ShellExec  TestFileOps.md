---
type: community
cohesion: 0.07
members: 40
---

# FileOps / ShellExec / TestFileOps

**Cohesion:** 0.07 - loosely connected
**Members:** 40 nodes

## Members
- [[.__init__()_1]] - code - loki/actions/file_ops.py
- [[.__init__()_2]] - code - loki/actions/shell_exec.py
- [[._build_tree()]] - code - loki/actions/file_ops.py
- [[._deny()]] - code - loki/actions/file_ops.py
- [[._is_allowed()]] - code - loki/actions/shell_exec.py
- [[._safe()]] - code - loki/actions/file_ops.py
- [[.create_file()]] - code - loki/actions/file_ops.py
- [[.create_folder()]] - code - loki/actions/file_ops.py
- [[.delete_file()]] - code - loki/actions/file_ops.py
- [[.delete_folder()]] - code - loki/actions/file_ops.py
- [[.execute()]] - code - loki/actions/shell_exec.py
- [[.move()]] - code - loki/actions/file_ops.py
- [[.test_allowed_echo()]] - code - loki/tests/test_actions.py
- [[.test_blocked_format()]] - code - loki/tests/test_actions.py
- [[.test_blocked_rm_rf()]] - code - loki/tests/test_actions.py
- [[.test_blocked_shutdown()]] - code - loki/tests/test_actions.py
- [[.test_confirm_action_executes()]] - code - loki/tests/test_voice_and_security.py
- [[.test_create_file()]] - code - loki/tests/test_actions.py
- [[.test_create_file_already_exists()]] - code - loki/tests/test_actions.py
- [[.test_create_file_outside_home_blocked()]] - code - loki/tests/test_actions.py
- [[.test_create_file_pushes_undo()]] - code - loki/tests/test_actions.py
- [[.test_delete_file()]] - code - loki/tests/test_actions.py
- [[.test_delete_nonexistent_file()]] - code - loki/tests/test_actions.py
- [[.test_empty_command()]] - code - loki/tests/test_actions.py
- [[.test_move_file()]] - code - loki/tests/test_actions.py
- [[Execute allowlisted shell commands safely.]] - rationale - loki/actions/shell_exec.py
- [[File operations — create, delete, move with security constraints and undo. Paths]] - rationale - loki/actions/file_ops.py
- [[FileOps]] - code - loki/actions/file_ops.py
- [[Returns (is_safe, resolved_path). Prevents path traversal outside trusted roots.]] - rationale - loki/actions/file_ops.py
- [[Secure filefolder operations with undo support.]] - rationale - loki/actions/file_ops.py
- [[Shell executor — allowlisted command execution with injection prevention.]] - rationale - loki/actions/shell_exec.py
- [[ShellExec]] - code - loki/actions/shell_exec.py
- [[TestFileOps]] - code - loki/tests/test_actions.py
- [[TestShellExec]] - code - loki/tests/test_actions.py
- [[file_ops()]] - code - loki/tests/test_actions.py
- [[file_ops.py]] - code - loki/actions/file_ops.py
- [[shell_exec()]] - code - loki/tests/test_actions.py
- [[shell_exec.py]] - code - loki/actions/shell_exec.py
- [[test_actions.py]] - code - loki/tests/test_actions.py
- [[undo()]] - code - loki/tests/test_actions.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/FileOps_/_ShellExec_/_TestFileOps
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_LokiApplication  ._init_all()  .__init__()]]
- 3 edges to [[_COMMUNITY_FakeTTS  ProcessManager  TestProcessManagerExactMatch]]
- 2 edges to [[_COMMUNITY_PendingActionStore  TestPendingActions  .is_expired()]]
- 1 edge to [[_COMMUNITY_TestConversationStateMachine  ._make_sm()  .test_end_conversation_goes_to_idle]]
- 1 edge to [[_COMMUNITY_WebSummarizer  TestSSRFProtection  _is_ssrf_risk()]]
- 1 edge to [[_COMMUNITY_ClipboardSync  TestClipboardSyncToken  .stop()]]
- 1 edge to [[_COMMUNITY_VoicePipeline  TestVoicePipeline  ._make()]]
- 1 edge to [[_COMMUNITY_ActionRouter  ._handle_agent_cancel()  ._handle_agent_run()]]

## Top bridge nodes
- [[FileOps]] - degree 25, connects to 7 communities
- [[.test_confirm_action_executes()]] - degree 3, connects to 2 communities
- [[ShellExec]] - degree 10, connects to 1 community