---
type: community
cohesion: 1.00
members: 2
---

# Focus Mode (hosts file site blocking)

**Cohesion:** 1.00 - tightly connected
**Members:** 2 nodes

## Members
- [[Config focus_mode block_sites (YouTubeRedditTwitterFacebookInstagramTikTokTwitchNetflix)]] - document - loki/config.yaml
- [[Focus Mode (hosts file site blocking)]] - document - LokiPRD.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Focus_Mode_hosts_file_site_blocking
SORT file.name ASC
```
