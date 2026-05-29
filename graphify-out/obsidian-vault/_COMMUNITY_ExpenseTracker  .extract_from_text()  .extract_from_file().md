---
type: community
cohesion: 0.13
members: 22
---

# ExpenseTracker / .extract_from_text() / .extract_from_file()

**Cohesion:** 0.13 - loosely connected
**Members:** 22 nodes

## Members
- [[.__init__()_29]] - code - loki/features/expense_tracker.py
- [[._append_row()]] - code - loki/features/expense_tracker.py
- [[._ensure_ledger()]] - code - loki/features/expense_tracker.py
- [[._llm()_1]] - code - loki/features/expense_tracker.py
- [[.extract_from_file()]] - code - loki/features/expense_tracker.py
- [[.extract_from_text()]] - code - loki/features/expense_tracker.py
- [[.get_ledger_path()]] - code - loki/features/expense_tracker.py
- [[.list_expenses()]] - code - loki/features/expense_tracker.py
- [[.monthly_summary()]] - code - loki/features/expense_tracker.py
- [[.scan_folder()]] - code - loki/features/expense_tracker.py
- [[ExpenseTracker]] - code - loki/features/expense_tracker.py
- [[ExpenseTracker — extract billing info from email text  .eml files and maintain]] - rationale - loki/features/expense_tracker.py
- [[Extract amount, currency, date, vendor from text using regex.]] - rationale - loki/features/expense_tracker.py
- [[Extract expense from an .eml or .txt receipt file.]] - rationale - loki/features/expense_tracker.py
- [[Extract expense from raw emailreceipt text and save to ledger.]] - rationale - loki/features/expense_tracker.py
- [[Extract plain text from an .eml file.]] - rationale - loki/features/expense_tracker.py
- [[List expenses from the ledger, optionally filtered by month (YYYY-MM).]] - rationale - loki/features/expense_tracker.py
- [[Scan a folder for .eml receipt files and extract all expenses.]] - rationale - loki/features/expense_tracker.py
- [[Summarize expenses by month and category.]] - rationale - loki/features/expense_tracker.py
- [[_heuristic_extract()]] - code - loki/features/expense_tracker.py
- [[_parse_eml()]] - code - loki/features/expense_tracker.py
- [[expense_tracker.py]] - code - loki/features/expense_tracker.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ExpenseTracker_/_extract_from_text_/_extract_from_file
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  DailyBriefing  .generate()]]
- 1 edge to [[_COMMUNITY_LokiBrain  test_brain.py  .ask()]]

## Top bridge nodes
- [[ExpenseTracker]] - degree 14, connects to 3 communities