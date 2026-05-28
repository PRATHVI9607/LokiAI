---
type: community
cohesion: 0.14
members: 20
---

# CalendarManager / ._load_events() / calendar_manager.py

**Cohesion:** 0.14 - loosely connected
**Members:** 20 nodes

## Members
- [[.__init__()_16]] - code - loki/features/calendar_manager.py
- [[._llm()]] - code - loki/features/calendar_manager.py
- [[._load_events()]] - code - loki/features/calendar_manager.py
- [[.find_conflicts()]] - code - loki/features/calendar_manager.py
- [[.import_ics()]] - code - loki/features/calendar_manager.py
- [[.list_events()]] - code - loki/features/calendar_manager.py
- [[.suggest_alternatives()]] - code - loki/features/calendar_manager.py
- [[CalendarManager]] - code - loki/features/calendar_manager.py
- [[CalendarManager — parse local .ics calendar files, detect scheduling conflicts,]] - rationale - loki/features/calendar_manager.py
- [[Detect overlapping calendar events.]] - rationale - loki/features/calendar_manager.py
- [[List calendar events in the next N days.]] - rationale - loki/features/calendar_manager.py
- [[Load and validate an ICS file, returning event count.]] - rationale - loki/features/calendar_manager.py
- [[Load events from an ICS file. Returns (events, source_path).]] - rationale - loki/features/calendar_manager.py
- [[Parse an ICS text into a list of event dicts.]] - rationale - loki/features/calendar_manager.py
- [[Parse iCalendar datetime strings.]] - rationale - loki/features/calendar_manager.py
- [[Suggest free time slots for a meeting given existing calendar.]] - rationale - loki/features/calendar_manager.py
- [[_find_ics_files()]] - code - loki/features/calendar_manager.py
- [[_parse_dt()]] - code - loki/features/calendar_manager.py
- [[_parse_ics()]] - code - loki/features/calendar_manager.py
- [[calendar_manager.py]] - code - loki/features/calendar_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/CalendarManager_/__load_events_/_calendar_managerpy
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  main.py]]
- 1 edge to [[_COMMUNITY_ConversationManager  .process_input()  ._speak()]]
- 1 edge to [[_COMMUNITY_LokiBrain  ApiMocker  FactChecker]]

## Top bridge nodes
- [[CalendarManager]] - degree 12, connects to 3 communities