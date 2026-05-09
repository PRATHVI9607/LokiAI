"""
Encrypted vault — AES-256-GCM encrypted key-value storage.
Master password set on first use.
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    import base64
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    logger.warning("cryptography not available: pip install cryptography")


class Vault:
    """AES-256-GCM encrypted key-value vault."""

    PBKDF2_ITERATIONS = 310000
    SALT_SIZE = 32
    NONCE_SIZE = 12

    def __init__(self, vault_path: Path):
        self._path = vault_path
        self._key: Optional[bytes] = None
        self._data: Dict[str, str] = {}

    def _derive_key(self, password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.PBKDF2_ITERATIONS,
        )
        return kdf.derive(password.encode("utf-8"))

    def unlock(self, password: str) -> Dict[str, Any]:
        if not CRYPTO_AVAILABLE:
            return {"success": False, "message": "cryptography library not installed."}

        if self._path.exists():
            try:
                raw = self._path.read_bytes()
                salt = raw[:self.SALT_SIZE]
                nonce = raw[self.SALT_SIZE:self.SALT_SIZE + self.NONCE_SIZE]
                ciphertext = raw[self.SALT_SIZE + self.NONCE_SIZE:]

                key = self._derive_key(password, salt)
                aesgcm = AESGCM(key)
                plaintext = aesgcm.decrypt(nonce, ciphertext, None)
                self._data = json.loads(plaintext.decode("utf-8"))
                self._key = key
                return {"success": True, "message": f"Vault unlocked. {len(self._data)} entries."}
            except Exception:
                return {"success": False, "message": "Wrong password or corrupted vault."}
        else:
            salt = os.urandom(self.SALT_SIZE)
            self._key = self._derive_key(password, salt)
            self._data = {}
            self._save(salt)
            return {"success": True, "message": "New vault created and unlocked."}

    def _save(self, salt: Optional[bytes] = None) -> None:
        if self._key is None:
            return
        if salt is None and self._path.exists():
            salt = self._path.read_bytes()[:self.SALT_SIZE]
        if salt is None:
            salt = os.urandom(self.SALT_SIZE)

        nonce = os.urandom(self.NONCE_SIZE)
        aesgcm = AESGCM(self._key)
        plaintext = json.dumps(self._data, ensure_ascii=False).encode("utf-8")
        ciphertext = aesgcm.encrypt(nonce, plaintext, None)

        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_bytes(salt + nonce + ciphertext)

    def store(self, key: str, value: str) -> Dict[str, Any]:
        if not CRYPTO_AVAILABLE:
            return {"success": False, "message": "cryptography not installed."}
        if self._key is None:
            return {"success": False, "message": "Vault is locked. Unlock it first."}
        if not key:
            return {"success": False, "message": "Key required."}

        self._data[key] = value
        self._save()
        return {"success": True, "message": f"Stored '{key}' in vault."}

    def retrieve(self, key: str) -> Dict[str, Any]:
        if not CRYPTO_AVAILABLE:
            return {"success": False, "message": "cryptography not installed."}
        if self._key is None:
            return {"success": False, "message": "Vault is locked."}
        if key not in self._data:
            return {"success": False, "message": f"No entry for '{key}' in vault."}

        return {"success": True, "message": f"Retrieved '{key}'.", "data": self._data[key]}

    def list_keys(self) -> Dict[str, Any]:
        if self._key is None:
            return {"success": False, "message": "Vault is locked."}
        keys = list(self._data.keys())
        if not keys:
            return {"success": True, "message": "Vault is empty."}
        return {"success": True, "message": f"Vault keys: {', '.join(keys)}", "data": keys}

    def delete(self, key: str) -> Dict[str, Any]:
        if self._key is None:
            return {"success": False, "message": "Vault is locked."}
        if key not in self._data:
            return {"success": False, "message": f"Key '{key}' not found."}
        del self._data[key]
        self._save()
        return {"success": True, "message": f"Deleted '{key}' from vault."}

    @property
    def is_locked(self) -> bool:
        return self._key is None
