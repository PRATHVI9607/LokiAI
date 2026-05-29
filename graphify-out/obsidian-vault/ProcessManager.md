---
source_file: "loki/features/process_manager.py"
type: "code"
community: "ProcessManager / TestProcessManagerExactMatch / process_manager.py"
location: "L27"
tags:
  - graphify/code
  - graphify/INFERRED
  - community/ProcessManager_/_TestProcessManagerExactMatch_/_process_managerpy
---

# ProcessManager

## Connections
- [[._init_all()]] - `calls` [INFERRED]
- [[.kill()]] - `method` [EXTRACTED]
- [[.list_processes()]] - `method` [EXTRACTED]
- [[.test_nonexistent_returns_no_process()]] - `calls` [INFERRED]
- [[.test_substring_returns_candidates_not_kills()]] - `calls` [INFERRED]
- [[FakeTTS]] - `uses` [INFERRED]
- [[List and terminate processes with safety guards.]] - `rationale_for` [EXTRACTED]
- [[LokiApplication]] - `uses` [INFERRED]
- [[TestClipboardSyncToken]] - `uses` [INFERRED]
- [[TestConversationStateMachine]] - `uses` [INFERRED]
- [[TestPendingActions]] - `uses` [INFERRED]
- [[TestProcessManagerExactMatch]] - `uses` [INFERRED]
- [[TestSSRFProtection]] - `uses` [INFERRED]
- [[TestTTSDrain]] - `uses` [INFERRED]
- [[TestVoicePipeline]] - `uses` [INFERRED]
- [[process_manager.py]] - `contains` [EXTRACTED]

#graphify/code #graphify/INFERRED #community/ProcessManager_/_TestProcessManagerExactMatch_/_process_managerpy