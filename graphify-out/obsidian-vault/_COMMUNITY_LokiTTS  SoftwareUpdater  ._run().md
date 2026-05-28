---
type: community
cohesion: 0.10
members: 30
---

# LokiTTS / SoftwareUpdater / ._run()

**Cohesion:** 0.10 - loosely connected
**Members:** 30 nodes

## Members
- [[.__init__()_11]] - code - loki/core/tts.py
- [[.__init__()_45]] - code - loki/features/software_updater.py
- [[._check_winget()]] - code - loki/features/software_updater.py
- [[._init_pyttsx3()]] - code - loki/core/tts.py
- [[._play_audio()]] - code - loki/core/tts.py
- [[._queue_worker()]] - code - loki/core/tts.py
- [[._run()]] - code - loki/features/software_updater.py
- [[._speak_edge()]] - code - loki/core/tts.py
- [[._speak_pyttsx3()]] - code - loki/core/tts.py
- [[.check_updates()]] - code - loki/features/software_updater.py
- [[.install_package()]] - code - loki/features/software_updater.py
- [[.speak()]] - code - loki/core/tts.py
- [[.stop()]] - code - loki/core/tts.py
- [[.update_all()]] - code - loki/features/software_updater.py
- [[.update_package()]] - code - loki/features/software_updater.py
- [[Enqueue text for speaking. Never drops messages.]] - rationale - loki/core/tts.py
- [[Install a package by name.]] - rationale - loki/features/software_updater.py
- [[List all packages with available upgrades.]] - rationale - loki/features/software_updater.py
- [[Loki TTS — edge-tts primary (Microsoft Neural), pyttsx3 fallback. Callback-base]] - rationale - loki/core/tts.py
- [[LokiTTS]] - code - loki/core/tts.py
- [[Single background thread — serializes all speech, signals when queue drains.]] - rationale - loki/core/tts.py
- [[SoftwareUpdater]] - code - loki/features/software_updater.py
- [[SoftwareUpdater — check and apply updates via winget (Windows Package Manager).]] - rationale - loki/features/software_updater.py
- [[Text-to-speech engine with edge-tts primary, pyttsx3 fallback.      Uses a que]] - rationale - loki/core/tts.py
- [[Upgrade a specific package by name or ID.]] - rationale - loki/features/software_updater.py
- [[Upgrade all installed packages.]] - rationale - loki/features/software_updater.py
- [[create_tts_engine()]] - code - loki/core/tts.py
- [[is_speaking()]] - code - loki/core/tts.py
- [[software_updater.py]] - code - loki/features/software_updater.py
- [[tts.py]] - code - loki/core/tts.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/LokiTTS_/_SoftwareUpdater_/__run
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_LokiApplication  ._init_all()  main.py]]
- 1 edge to [[_COMMUNITY_ConversationManager  .process_input()  ._speak()]]

## Top bridge nodes
- [[SoftwareUpdater]] - degree 11, connects to 2 communities
- [[create_tts_engine()]] - degree 3, connects to 1 community