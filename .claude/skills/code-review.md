# Code Review Skill for Loki

## Trigger
When asked to review code in the Loki project.

## Checklist
1. **Security**: Path traversal, command injection, hardcoded secrets
2. **Return format**: All feature methods return `{"success": bool, "message": str, "data": Any}`
3. **Error handling**: Every external call wrapped in try/except with logger.error
4. **Threading**: No direct UI calls from background threads — use Qt signals
5. **Imports**: Optional imports (psutil, cryptography) guarded with try/except + `_AVAILABLE` flag
6. **Memory**: No memory leaks (close files, stop threads on shutdown)
7. **Personality**: Loki responses are witty and brief — not generic

## Auto-fixes
- Missing `logger.error` on exception → add it
- Bare `except:` → change to `except Exception as e:`
- Missing return type hints on public methods → add them
- `print()` statements → replace with `logger.info/debug`
