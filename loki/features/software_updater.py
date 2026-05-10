"""
SoftwareUpdater — check and apply updates via winget (Windows Package Manager).
"""

import logging
import subprocess
import shutil
from typing import Optional

logger = logging.getLogger(__name__)


class SoftwareUpdater:
    def __init__(self):
        self._winget = shutil.which("winget")

    def _run(self, args: list[str], timeout: int = 120) -> tuple[int, str, str]:
        try:
            result = subprocess.run(
                args, capture_output=True, text=True, timeout=timeout,
                encoding="utf-8", errors="replace",
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out."
        except Exception as e:
            return -1, "", str(e)

    def _check_winget(self) -> Optional[dict]:
        if not self._winget:
            return {
                "success": False,
                "message": "winget (Windows Package Manager) is not available. Install it from the Microsoft Store.",
            }
        return None

    def check_updates(self) -> dict:
        """List all packages with available upgrades."""
        err = self._check_winget()
        if err:
            return err
        code, stdout, stderr = self._run(["winget", "upgrade", "--include-unknown"], timeout=60)
        if code != 0 and not stdout:
            return {"success": False, "message": f"Could not check updates: {stderr[:200]}"}
        lines = [l for l in stdout.splitlines() if l.strip() and not l.startswith("-")]
        # Skip header lines
        packages = []
        header_passed = False
        for line in lines:
            if "Name" in line and "Id" in line and "Version" in line:
                header_passed = True
                continue
            if header_passed and line.strip():
                packages.append(line.strip())

        if not packages:
            return {"success": True, "message": "All software is up to date.", "data": {"packages": []}}

        msg = f"{len(packages)} update(s) available:\n" + "\n".join(f"  • {p}" for p in packages[:15])
        return {"success": True, "message": msg, "data": {"packages": packages}}

    def update_all(self) -> dict:
        """Upgrade all installed packages."""
        err = self._check_winget()
        if err:
            return err
        code, stdout, stderr = self._run(
            ["winget", "upgrade", "--all", "--include-unknown", "--silent", "--accept-package-agreements", "--accept-source-agreements"],
            timeout=300,
        )
        if code not in (0, 1):  # winget returns 1 for "no upgrades"
            return {"success": False, "message": f"Update failed: {stderr[:300]}"}
        return {"success": True, "message": "All packages updated successfully.", "data": {"output": stdout[-500:]}}

    def update_package(self, package_name: str) -> dict:
        """Upgrade a specific package by name or ID."""
        err = self._check_winget()
        if err:
            return err
        if not package_name.strip():
            return {"success": False, "message": "Specify a package name to update."}
        code, stdout, stderr = self._run(
            ["winget", "upgrade", package_name, "--silent", "--accept-package-agreements", "--accept-source-agreements"],
            timeout=180,
        )
        if code == 0:
            return {"success": True, "message": f"{package_name} updated successfully.", "data": {"output": stdout[-300:]}}
        return {"success": False, "message": f"Could not update {package_name}: {(stderr or stdout)[-200:]}"}

    def install_package(self, package_name: str) -> dict:
        """Install a package by name."""
        err = self._check_winget()
        if err:
            return err
        code, stdout, stderr = self._run(
            ["winget", "install", package_name, "--silent", "--accept-package-agreements", "--accept-source-agreements"],
            timeout=180,
        )
        if code == 0:
            return {"success": True, "message": f"{package_name} installed successfully.", "data": {}}
        return {"success": False, "message": f"Could not install {package_name}: {(stderr or stdout)[-200:]}"}
