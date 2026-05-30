---
type: community
cohesion: 0.25
members: 8
---

# ScreenshotSearch.locate_text (click / ComputerControl.click_text (OCR cli / ComputerControl.read_screen

**Cohesion:** 0.25 - loosely connected
**Members:** 8 nodes

## Members
- [[ComputerControl.click_text (OCR click)]] - code - loki/actions/computer_control.py
- [[ComputerControl.read_screen]] - code - loki/actions/computer_control.py
- [[Rationale WinRT-OCR-first (no Tesseract install needed)]] - code - loki/features/screenshot_search.py
- [[ScreenshotSearch (OCRScreen Reader)]] - code - loki/features/screenshot_search.py
- [[ScreenshotSearch.capture_and_read]] - code - loki/features/screenshot_search.py
- [[ScreenshotSearch.locate_text (click-center {x,y})]] - code - loki/features/screenshot_search.py
- [[_word_boxes_tesseract (pytesseract fallback)]] - code - loki/features/screenshot_search.py
- [[_word_boxes_winrt (WinRT OCR word boxes)]] - code - loki/features/screenshot_search.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ScreenshotSearchlocate_text_click_/_ComputerControlclick_text_OCR_cli_/_ComputerControlread_screen
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_ComputerControl (Desktop Control En  pyautogui FAILSAFE (corner-abort sa  ComputerControl.click]]

## Top bridge nodes
- [[ComputerControl.click_text (OCR click)]] - degree 2, connects to 1 community
- [[ComputerControl.read_screen]] - degree 2, connects to 1 community