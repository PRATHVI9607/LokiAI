"""
Security scanner — detect API keys, secrets, and vulnerabilities in code.
"""

import re
import logging
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

DEFAULT_PATTERNS = [
    {"name": "API Key", "regex": r'(?i)(api[_-]?key|apikey)\s*[=:]\s*["\']?[A-Za-z0-9_\-]{20,}["\']?'},
    {"name": "AWS Access Key", "regex": r'AKIA[0-9A-Z]{16}'},
    {"name": "AWS Secret Key", "regex": r'(?i)aws.{0,20}secret.{0,20}[=:]\s*["\']?[A-Za-z0-9/+]{40}["\']?'},
    {"name": "Private Key", "regex": r'-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----'},
    {"name": "Password in Code", "regex": r'(?i)(password|passwd|pwd)\s*[=:]\s*["\'][^"\']{6,}["\']'},
    {"name": "Bearer Token", "regex": r'Bearer\s+[A-Za-z0-9\-._~+/]+=*'},
    {"name": "GitHub Token", "regex": r'ghp_[A-Za-z0-9]{36}'},
    {"name": "OpenAI Key", "regex": r'sk-[A-Za-z0-9]{48}'},
    {"name": "Slack Token", "regex": r'xox[baprs]-[A-Za-z0-9\-]{10,}'},
    {"name": "Google API Key", "regex": r'AIza[0-9A-Za-z\-_]{35}'},
    {"name": "Hardcoded IP", "regex": r'(?<![.\d])(192\.168\.|10\.\d+\.|172\.(1[6-9]|2\d|3[01])\.)\d+\.\d+'},
    {"name": "SQL Injection Risk", "regex": r'["\'].*(\+|%)\s*(query|sql|statement)'},
    {"name": "Debug Print with Secret", "regex": r'print\(.*(?:password|secret|key|token).*\)'},
]

SKIP_EXTENSIONS = {".pyc", ".pyo", ".exe", ".dll", ".so", ".bin", ".jpg",
                    ".jpeg", ".png", ".gif", ".pdf", ".zip", ".rar", ".7z"}

SKIP_DIRS = {"__pycache__", ".git", "node_modules", "venv", ".venv", ".tox",
              "dist", "build", ".pytest_cache"}


class SecurityScanner:
    """Scan code files for secrets and security vulnerabilities."""

    def __init__(self, patterns: List[Dict] = None):
        self._patterns = []
        for p in (patterns or DEFAULT_PATTERNS):
            try:
                compiled = re.compile(p["regex"])
                self._patterns.append({"name": p["name"], "regex": compiled})
            except re.error as e:
                logger.error(f"Invalid pattern '{p['name']}': {e}")

    def scan(self, path: str = ".") -> Dict[str, Any]:
        scan_path = Path(path).expanduser().resolve()
        if not scan_path.exists():
            return {"success": False, "message": f"Path not found: {scan_path}"}

        findings = []

        if scan_path.is_file():
            findings = self._scan_file(scan_path)
        else:
            for fpath in self._iter_files(scan_path):
                findings.extend(self._scan_file(fpath))

        if not findings:
            return {"success": True, "message": f"Scan complete. No secrets detected in {scan_path.name}. Clean.", "data": []}

        lines = [f"⚠ Security scan found {len(findings)} issue(s) in {scan_path.name}:"]
        for f in findings[:20]:
            lines.append(f"  [{f['type']}] {f['file']}:{f['line']} — {f['preview']}")
        if len(findings) > 20:
            lines.append(f"  ... and {len(findings) - 20} more.")

        return {"success": True, "message": "\n".join(lines), "data": findings}

    def _iter_files(self, directory: Path):
        for root, dirs, files in directory.walk() if hasattr(directory, 'walk') else self._os_walk(directory):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
            for fname in files:
                fpath = Path(root) / fname
                if fpath.suffix.lower() not in SKIP_EXTENSIONS:
                    yield fpath

    def _os_walk(self, directory: Path):
        import os
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
            yield Path(root), dirs, files

    def _scan_file(self, path: Path) -> List[Dict]:
        results = []
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
            for i, line in enumerate(content.splitlines(), 1):
                for pattern in self._patterns:
                    if pattern["regex"].search(line):
                        preview = line.strip()[:60]
                        results.append({
                            "type": pattern["name"],
                            "file": str(path),
                            "line": i,
                            "preview": preview,
                        })
        except Exception:
            pass
        return results
