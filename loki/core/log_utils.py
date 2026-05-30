"""
Log-sanitisation helpers (issue #76).

URLs and free text can carry secrets — `?api_key=…`, `token=…`, `Bearer …`.
`redact()` masks those before they reach the log file, so a shared log never
leaks credentials.
"""

import re

# key=value pairs where the key looks sensitive (query strings, form data)
_KV_RE = re.compile(
    r"(?i)\b(api[_-]?key|access[_-]?token|token|secret|password|passwd|pwd|auth|"
    r"client[_-]?secret|sig|signature)=([^&\s]+)"
)
# Bearer / Basic auth headers
_BEARER_RE = re.compile(r"(?i)\b(bearer|basic)\s+[A-Za-z0-9._\-+/=]{8,}")


def redact(text: str) -> str:
    """Mask obvious secrets in a string for safe logging."""
    if not text:
        return text
    out = _KV_RE.sub(lambda m: f"{m.group(1)}=***", text)
    out = _BEARER_RE.sub(lambda m: f"{m.group(1)} ***", out)
    return out
