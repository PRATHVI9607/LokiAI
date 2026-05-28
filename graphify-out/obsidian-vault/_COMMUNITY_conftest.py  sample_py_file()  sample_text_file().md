---
type: community
cohesion: 0.40
members: 5
---

# conftest.py / sample_py_file() / sample_text_file()

**Cohesion:** 0.40 - moderately connected
**Members:** 5 nodes

## Members
- [[conftest.py]] - code - loki/tests/conftest.py
- [[sample_py_file()]] - code - loki/tests/conftest.py
- [[sample_text_file()]] - code - loki/tests/conftest.py
- [[tmp_dir()]] - code - loki/tests/conftest.py
- [[tmp_home()]] - code - loki/tests/conftest.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/conftestpy_/_sample_py_file_/_sample_text_file
SORT file.name ASC
```
