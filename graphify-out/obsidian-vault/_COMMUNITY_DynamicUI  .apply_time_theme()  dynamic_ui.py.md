---
type: community
cohesion: 0.11
members: 23
---

# DynamicUI / .apply_time_theme() / dynamic_ui.py

**Cohesion:** 0.11 - loosely connected
**Members:** 23 nodes

## Members
- [[.__init__()_26]] - code - loki/features/dynamic_ui.py
- [[._get_period_theme()]] - code - loki/features/dynamic_ui.py
- [[._write_state()]] - code - loki/features/dynamic_ui.py
- [[.apply_mood_theme()]] - code - loki/features/dynamic_ui.py
- [[.apply_time_theme()]] - code - loki/features/dynamic_ui.py
- [[.get_current_theme()]] - code - loki/features/dynamic_ui.py
- [[.list_themes()]] - code - loki/features/dynamic_ui.py
- [[.set_wallpaper()]] - code - loki/features/dynamic_ui.py
- [[.start_auto_theme()]] - code - loki/features/dynamic_ui.py
- [[.stop_auto_theme()]] - code - loki/features/dynamic_ui.py
- [[Apply a mood-based theme.]] - rationale - loki/features/dynamic_ui.py
- [[Apply the theme appropriate for the current time of day.]] - rationale - loki/features/dynamic_ui.py
- [[Create a solid-color BMP as a wallpaper using Pillow.]] - rationale - loki/features/dynamic_ui.py
- [[DynamicUI]] - code - loki/features/dynamic_ui.py
- [[DynamicUI — change Windows wallpaper and push theme tokens based on time of day,]] - rationale - loki/features/dynamic_ui.py
- [[List all available themes.]] - rationale - loki/features/dynamic_ui.py
- [[Read the current active theme state.]] - rationale - loki/features/dynamic_ui.py
- [[Set a custom wallpaper from a file path.]] - rationale - loki/features/dynamic_ui.py
- [[Start a background thread that auto-applies time-based theme every 30 minutes.]] - rationale - loki/features/dynamic_ui.py
- [[Stop the auto-theme background thread.]] - rationale - loki/features/dynamic_ui.py
- [[_create_solid_bmp()]] - code - loki/features/dynamic_ui.py
- [[_set_wallpaper_path()]] - code - loki/features/dynamic_ui.py
- [[dynamic_ui.py]] - code - loki/features/dynamic_ui.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/DynamicUI_/_apply_time_theme_/_dynamic_uipy
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  BrowserCtrl  DailyBriefing]]

## Top bridge nodes
- [[DynamicUI]] - degree 13, connects to 2 communities