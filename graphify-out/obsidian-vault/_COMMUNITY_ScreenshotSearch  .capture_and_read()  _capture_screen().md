---
type: community
cohesion: 0.14
members: 22
---

# ScreenshotSearch / .capture_and_read() / _capture_screen()

**Cohesion:** 0.14 - loosely connected
**Members:** 22 nodes

## Members
- [[.__init__()_45]] - code - loki/features/screenshot_search.py
- [[._llm()_5]] - code - loki/features/screenshot_search.py
- [[._ocr()]] - code - loki/features/screenshot_search.py
- [[.capture_and_read()]] - code - loki/features/screenshot_search.py
- [[.describe_screen()]] - code - loki/features/screenshot_search.py
- [[.save_screenshot()]] - code - loki/features/screenshot_search.py
- [[.search_screen()]] - code - loki/features/screenshot_search.py
- [[.translate_screen()]] - code - loki/features/screenshot_search.py
- [[Capture and save screenshot to disk.]] - rationale - loki/features/screenshot_search.py
- [[Capture screen as PNG bytes. Returns None on failure.]] - rationale - loki/features/screenshot_search.py
- [[Capture screen, OCR it, and translate all text to target language.]] - rationale - loki/features/screenshot_search.py
- [[Capture screen, OCR it, then search for query text.]] - rationale - loki/features/screenshot_search.py
- [[Capture the screen (or a region) and extract all visible text via OCR.]] - rationale - loki/features/screenshot_search.py
- [[Capture the screen and ask LLM to describe what's on it (vision model).]] - rationale - loki/features/screenshot_search.py
- [[ScreenshotSearch]] - code - loki/features/screenshot_search.py
- [[ScreenshotSearch — capture screen  region, extract text via OCR, and optionally]] - rationale - loki/features/screenshot_search.py
- [[Use Windows built-in OCR via PowerShell WinRT (Windows 10+).]] - rationale - loki/features/screenshot_search.py
- [[Use pytesseract if available.]] - rationale - loki/features/screenshot_search.py
- [[_capture_screen()]] - code - loki/features/screenshot_search.py
- [[_ocr_tesseract()]] - code - loki/features/screenshot_search.py
- [[_ocr_windows()]] - code - loki/features/screenshot_search.py
- [[screenshot_search.py]] - code - loki/features/screenshot_search.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ScreenshotSearch_/_capture_and_read_/__capture_screen
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  BrowserCtrl  DailyBriefing]]
- 1 edge to [[_COMMUNITY_LokiBrain  DailyBriefing  CodeAssistant]]

## Top bridge nodes
- [[ScreenshotSearch]] - degree 12, connects to 3 communities