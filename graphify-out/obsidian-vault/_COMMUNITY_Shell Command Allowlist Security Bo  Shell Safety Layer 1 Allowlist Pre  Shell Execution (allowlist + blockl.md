---
type: community
cohesion: 0.17
members: 12
---

# Shell Command Allowlist Security Bo / Shell Safety Layer 1: Allowlist Pre / Shell Execution (allowlist + blockl

**Cohesion:** 0.17 - loosely connected
**Members:** 12 nodes

## Members
- [[Allowlist Development Commands (gitpythonpipnpmnodenpxcargogodotnetmakecmakepytestjest)]] - document - loki/data/command_allowlist.txt
- [[Allowlist Editors Launch Only (codenotepadnotepad++nanovim)]] - document - loki/data/command_allowlist.txt
- [[Allowlist Filesystem Commands (dirlspwdcdtypecatechocopyxcopyrobocopymkdirmd)]] - document - loki/data/command_allowlist.txt
- [[Allowlist Package Manager Commands (wingetchocoscoop)]] - document - loki/data/command_allowlist.txt
- [[Allowlist PowerShell Read-Only (Get- and Write- prefixes only)]] - document - loki/data/command_allowlist.txt
- [[Allowlist System Info Read-Only Commands (ipconfignetstattasklistsysteminfoverwhoamihostnamepingtracertnslookupcurlwget)]] - document - loki/data/command_allowlist.txt
- [[Allowlist Text Processing Commands (findstrgrepsortfind)]] - document - loki/data/command_allowlist.txt
- [[Rationale Allowlist in Plain Text File (admins can extend without code changes)]] - document - LokiPRD.md
- [[Shell Command Allowlist Security Boundary]] - document - loki/data/command_allowlist.txt
- [[Shell Execution (allowlist + blocklist two-layer)]] - document - LokiPRD.md
- [[Shell Safety Layer 1 Allowlist Prefix Matching]] - document - LokiPRD.md
- [[Shell Safety Layer 2 Block Dangerous Patterns]] - document - LokiPRD.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Shell_Command_Allowlist_Security_Bo_/_Shell_Safety_Layer_1_Allowlist_Pre_/_Shell_Execution_allowlist__blockl
SORT file.name ASC
```
