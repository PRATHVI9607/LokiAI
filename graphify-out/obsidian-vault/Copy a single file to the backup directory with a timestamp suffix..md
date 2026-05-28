---
source_file: "loki/features/backup_manager.py"
type: "rationale"
community: "BackupManager / .backup_directory() / .backup_file()"
location: "L21"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/BackupManager_/_backup_directory_/_backup_file
---

# Copy a single file to the backup directory with a timestamp suffix.

## Connections
- [[.backup_file()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/BackupManager_/_backup_directory_/_backup_file