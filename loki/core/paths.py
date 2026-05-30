"""
Shared path-safety helpers (issue #62 — DRY the validation that was duplicated
across FileOps and elsewhere).

`resolve_within_roots` is the single source of truth for "is this path inside a
trusted root, and what does it resolve to?" — used to block path traversal.
"""

from pathlib import Path
from typing import Iterable, Tuple


def resolve_within_roots(path: str, roots: Iterable[Path]) -> Tuple[bool, Path]:
    """Resolve `path` and return (is_inside_a_trusted_root, resolved_path).

    Symlinks/`..` are collapsed by `resolve()`, so traversal attempts land at
    their true location and are then checked against the roots.
    """
    if not path or not str(path).strip():
        return False, Path()
    try:
        resolved = Path(path).expanduser().resolve()
    except Exception:
        return False, Path()
    for root in roots:
        try:
            if resolved.is_relative_to(root):
                return True, resolved
        except Exception:
            continue
    return False, resolved
