---
type: community
cohesion: 0.22
members: 13
---

# DigitalDeclutter.find_duplicates / _SAFE_DIRS Whitelist (Downloads + D / DigitalDeclutter

**Cohesion:** 0.22 - loosely connected
**Members:** 13 nodes

## Members
- [[DEFAULT_RULES Extension Map]] - code - loki/features/file_organizer.py
- [[DigitalDeclutter_1]] - code - loki/features/digital_declutter.py
- [[DigitalDeclutter.find_duplicates]] - code - loki/features/digital_declutter.py
- [[DigitalDeclutter.find_large_files]] - code - loki/features/digital_declutter.py
- [[DigitalDeclutter.find_old_files]] - code - loki/features/digital_declutter.py
- [[DigitalDeclutter.suggest_cleanup]] - code - loki/features/digital_declutter.py
- [[FileOrganizer_1]] - code - loki/features/file_organizer.py
- [[FileOrganizer._is_safe_dir]] - code - loki/features/file_organizer.py
- [[FileOrganizer.organize]] - code - loki/features/file_organizer.py
- [[SKIP_DIRS Constant (gitcachenode_modules)]] - code - loki/features/digital_declutter.py
- [[TestFileOrganizer_1]] - test - loki/tests/test_features.py
- [[_SAFE_DIRS Whitelist (Downloads + Desktop only)]] - concept - loki/features/file_organizer.py
- [[tryexcept OSError around fp.stat()]] - concept - loki/features/digital_declutter.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/DigitalDeclutterfind_duplicates_/__SAFE_DIRS_Whitelist_Downloads__D_/_DigitalDeclutter
SORT file.name ASC
```
