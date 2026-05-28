---
source_file: "loki/core/brain_memory.py"
type: "rationale"
community: "BrainMemory / ._save_unlocked() / ._add_fact_unlocked()"
location: "L157"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/BrainMemory_/__save_unlocked_/__add_fact_unlocked
---

# Add one fact without acquiring lock. Caller must hold self._lock.

## Connections
- [[._add_fact_unlocked()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/BrainMemory_/__save_unlocked_/__add_fact_unlocked