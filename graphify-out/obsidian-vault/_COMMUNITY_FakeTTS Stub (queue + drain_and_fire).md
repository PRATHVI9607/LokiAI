---
type: community
cohesion: 0.67
members: 3
---

# FakeTTS Stub (queue + drain_and_fire)

**Cohesion:** 0.67 - moderately connected
**Members:** 3 nodes

## Members
- [[FakeTTS Stub (queue + drain_and_fire)]] - test - loki/tests/test_voice_and_security.py
- [[TestConversationStateMachine (state transitions + timeout)]] - test - loki/tests/test_voice_and_security.py
- [[TestTTSDrain (TTS queue drain + idle lifecycle)]] - test - loki/tests/test_voice_and_security.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/FakeTTS_Stub_queue__drain_and_fire
SORT file.name ASC
```
