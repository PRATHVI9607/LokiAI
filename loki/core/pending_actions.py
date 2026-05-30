"""
PendingAction — confirmation gate for destructive operations.

Destructive intents (delete, kill, shell, git-commit, install/update) are held
here instead of executing immediately. The router returns a confirmation prompt;
the user speaks/types "yes <token>" or "confirm" to execute, or "cancel" to drop.
"""

import os
import threading
import time
from dataclasses import dataclass, field
from typing import Dict, Optional

_TTL_SECONDS = 60  # pending actions expire after 60s
_MAX_PENDING = 50  # hard cap so a misbehaving caller can't grow the store unbounded


@dataclass
class PendingAction:
    token: str
    intent_name: str
    params: dict
    description: str
    expires_at: float = field(default_factory=lambda: time.time() + _TTL_SECONDS)

    def is_expired(self) -> bool:
        return time.time() > self.expires_at


class PendingActionStore:
    """Thread-safe store for pending confirmations."""

    def __init__(self):
        self._store: Dict[str, PendingAction] = {}
        self._lock = threading.Lock()
        self._last_token: Optional[str] = None  # most-recent pending action

    def push(self, intent_name: str, params: dict, description: str) -> PendingAction:
        token = os.urandom(3).hex()  # 6-char hex
        action = PendingAction(token=token, intent_name=intent_name, params=params, description=description)
        with self._lock:
            # Expire old entries lazily
            expired = [k for k, v in self._store.items() if v.is_expired()]
            for k in expired:
                del self._store[k]
            # Hard cap — drop the oldest if still over the limit after expiry
            while len(self._store) >= _MAX_PENDING:
                oldest = min(self._store, key=lambda k: self._store[k].expires_at)
                del self._store[oldest]
            self._store[token] = action
            self._last_token = token
        return action

    def pop(self, token: Optional[str] = None) -> Optional[PendingAction]:
        """Pop by token or most-recent if token is None."""
        with self._lock:
            if token is None:
                token = self._last_token
            if not token:
                return None
            action = self._store.pop(token, None)
            if action and action.is_expired():
                return None
            if token == self._last_token:
                self._last_token = None
            return action

    def peek_last(self) -> Optional[PendingAction]:
        with self._lock:
            if self._last_token:
                a = self._store.get(self._last_token)
                return a if a and not a.is_expired() else None
            return None

    def cancel_all(self) -> int:
        with self._lock:
            count = len(self._store)
            self._store.clear()
            self._last_token = None
        return count
