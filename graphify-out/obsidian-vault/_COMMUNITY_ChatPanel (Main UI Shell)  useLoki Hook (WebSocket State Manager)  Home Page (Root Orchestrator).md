---
type: community
cohesion: 0.20
members: 23
---

# ChatPanel (Main UI Shell) / useLoki Hook (WebSocket State Manager) / Home Page (Root Orchestrator)

**Cohesion:** 0.20 - loosely connected
**Members:** 23 nodes

## Members
- [[ChatMessage Type Definition]] - code - loki-ui/hooks/useLoki.ts
- [[ChatPanel (Main UI Shell)]] - code - loki-ui/components/ChatPanel.tsx
- [[FileEntry Type (filename + chunkCount)]] - code - loki-ui/hooks/useLoki.ts
- [[FilePanel (RAG File Upload Sidebar)]] - code - loki-ui/components/FilePanel.tsx
- [[Home Page (Root Orchestrator)]] - code - loki-ui/app/page.tsx
- [[InputBar (Text + Action Controls)]] - code - loki-ui/components/InputBar.tsx
- [[Loki Design Color Palette]] - code - loki-ui/tailwind.config.ts
- [[MessageBubble (Chat Message Renderer)]] - code - loki-ui/components/MessageBubble.tsx
- [[Next.js Config (Static Export)]] - code - loki-ui/next.config.mjs
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
TABLE source_file, type FROM #community/ChatPanel_Main_UI_Shell_/_useLoki_Hook_WebSocket_State_Manager_/_Home_Page_Root_Orchestrator
SORT file.name ASC
```
