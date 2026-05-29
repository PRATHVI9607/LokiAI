---
type: community
cohesion: 0.21
members: 20
---

# ChatPanel (Main UI Shell) / useLoki Hook (WebSocket State Manag / Status Type (idle/listening/thinkin

**Cohesion:** 0.21 - loosely connected
**Members:** 20 nodes

## Members
- [[ChatMessage Type Definition]] - code - loki-ui/hooks/useLoki.ts
- [[ChatPanel (Main UI Shell)]] - code - loki-ui/components/ChatPanel.tsx
- [[FileEntry Type (filename + chunkCount)]] - code - loki-ui/hooks/useLoki.ts
- [[FilePanel (RAG File Upload Sidebar)]] - code - loki-ui/components/FilePanel.tsx
- [[InputBar (Text + Action Controls)]] - code - loki-ui/components/InputBar.tsx
- [[Loki Design Color Palette]] - code - loki-ui/tailwind.config.ts
- [[Personality Type (lokijarvisfriday)]] - code - loki-ui/hooks/useLoki.ts
- [[PersonalityPicker (LokiJARVISFRIDAY Selector)]] - code - loki-ui/components/PersonalityPicker.tsx
- [[PostCSS Config]] - code - loki-ui/postcss.config.js
- [[RuneCanvas (Animated Background Particle System)]] - code - loki-ui/components/RuneCanvas.tsx
- [[Status Orb CSS Animations (orb-pulselistenthinkspeak)]] - code - loki-ui/tailwind.config.ts
- [[Status Type (idlelisteningthinkingspeakingoffline)]] - code - loki-ui/hooks/useLoki.ts
- [[StatusOrb (Status Indicator Pill)]] - code - loki-ui/components/StatusOrb.tsx
- [[Tailwind Config (Loki Design Tokens)]] - code - loki-ui/tailwind.config.ts
- [[WebSocket Connection Manager]] - code - loki-ui/hooks/useLoki.ts
- [[deleteFile (HTTP DELETE uploadfilename)]] - code - loki-ui/hooks/useLoki.ts
- [[refreshFiles (HTTP GET files)]] - code - loki-ui/hooks/useLoki.ts
- [[setPersonality (HTTP POST brainpersonality)]] - code - loki-ui/hooks/useLoki.ts
- [[uploadFile (HTTP POST upload)]] - code - loki-ui/hooks/useLoki.ts
- [[useLoki Hook (WebSocket State Manager)]] - code - loki-ui/hooks/useLoki.ts

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ChatPanel_Main_UI_Shell_/_useLoki_Hook_WebSocket_State_Manag_/_Status_Type_idle/listening/thinkin
SORT file.name ASC
```
