"""
FootprintAuditor — audit Windows privacy settings, installed apps with network access,
startup entries, and scheduled tasks to surface potential data-leaking activity.
"""

import logging
import subprocess
import winreg
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def _run_ps(cmd: str, timeout: int = 30) -> str:
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", cmd],
            capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="replace",
        )
        return result.stdout.strip()
    except Exception as e:
        logger.debug("PowerShell error: %s", e)
        return ""


class FootprintAuditor:
    def audit_startup(self) -> dict:
        """List all programs set to run at startup."""
        entries: list[dict] = []

        # Registry startup keys
        reg_paths = [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run"),
        ]
        for hive, key_path in reg_paths:
            try:
                with winreg.OpenKey(hive, key_path) as key:
                    i = 0
                    while True:
                        try:
                            name, value, _ = winreg.EnumValue(key, i)
                            entries.append({"name": name, "command": value, "source": "registry"})
                            i += 1
                        except OSError:
                            break
            except OSError:
                pass

        # Startup folder
        startup_dirs = [
            Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup",
            Path("C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Startup"),
        ]
        for sd in startup_dirs:
            if sd.exists():
                for f in sd.iterdir():
                    if f.is_file():
                        entries.append({"name": f.name, "command": str(f), "source": "startup_folder"})

        msg = f"Found {len(entries)} startup entries:\n"
        msg += "\n".join(f"  • {e['name']}: {e['command'][:80]}" for e in entries[:20])
        return {"success": True, "message": msg, "data": {"entries": entries}}

    def audit_scheduled_tasks(self) -> dict:
        """List scheduled tasks with network or file system triggers."""
        raw = _run_ps(
            "Get-ScheduledTask | Where-Object {$_.State -ne 'Disabled'} | "
            "Select-Object TaskName,TaskPath,@{n='Actions';e={$_.Actions.Execute -join ', '}} | "
            "ConvertTo-Json -Compress"
        )
        if not raw:
            return {"success": False, "message": "Could not retrieve scheduled tasks."}

        try:
            import json
            tasks_raw = json.loads(raw)
            if isinstance(tasks_raw, dict):
                tasks_raw = [tasks_raw]
            tasks = [
                {"name": t.get("TaskName", ""), "path": t.get("TaskPath", ""), "action": t.get("Actions", "")}
                for t in tasks_raw if isinstance(t, dict)
            ]
        except Exception:
            tasks = [{"name": "raw", "path": "", "action": raw[:500]}]

        suspicious = [t for t in tasks if any(
            kw in (t["action"] or "").lower()
            for kw in ["powershell", "cmd", "wscript", "mshta", "regsvr32", "rundll32"]
        )]

        msg = f"{len(tasks)} active scheduled tasks. {len(suspicious)} use shell interpreters:\n"
        msg += "\n".join(f"  ⚠ {t['name']}: {t['action'][:80]}" for t in suspicious[:10])
        return {"success": True, "message": msg, "data": {"tasks": tasks, "suspicious": suspicious}}

    def audit_privacy_settings(self) -> dict:
        """Check key Windows privacy registry settings."""
        checks: list[dict] = []

        privacy_keys = [
            (r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\location", "Location"),
            (r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\microphone", "Microphone"),
            (r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam", "Camera"),
            (r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\activity", "Activity History"),
        ]

        for key_path, label in privacy_keys:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
                    try:
                        val, _ = winreg.QueryValueEx(key, "Value")
                        status = "Enabled" if val == "Allow" else "Restricted"
                    except OSError:
                        status = "Unknown"
            except OSError:
                status = "Key not found"
            checks.append({"setting": label, "status": status})

        # Telemetry level
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\DataCollection") as key:
                try:
                    val, _ = winreg.QueryValueEx(key, "AllowTelemetry")
                    levels = {0: "Security (off)", 1: "Basic", 2: "Enhanced", 3: "Full"}
                    checks.append({"setting": "Telemetry", "status": levels.get(val, str(val))})
                except OSError:
                    checks.append({"setting": "Telemetry", "status": "Policy not set (default: Full)"})
        except OSError:
            checks.append({"setting": "Telemetry", "status": "Policy not set (default: Full)"})

        msg = "Windows Privacy Settings:\n" + "\n".join(f"  {c['setting']}: {c['status']}" for c in checks)
        return {"success": True, "message": msg, "data": {"settings": checks}}

    def audit_network_listeners(self) -> dict:
        """List processes with active network listeners."""
        raw = _run_ps(
            "Get-NetTCPConnection -State Listen | "
            "Select-Object LocalPort,@{n='Process';e={(Get-Process -Id $_.OwningProcess -EA SilentlyContinue).Name}} | "
            "Sort-Object LocalPort | ConvertTo-Json -Compress"
        )
        if not raw:
            return {"success": False, "message": "Could not retrieve network listeners."}

        try:
            import json
            listeners_raw = json.loads(raw)
            if isinstance(listeners_raw, dict):
                listeners_raw = [listeners_raw]
            listeners = [
                {"port": l.get("LocalPort"), "process": l.get("Process", "unknown")}
                for l in listeners_raw if isinstance(l, dict)
            ]
        except Exception:
            listeners = []

        msg = f"{len(listeners)} active network listeners:\n"
        msg += "\n".join(f"  Port {l['port']}: {l['process']}" for l in listeners[:20])
        return {"success": True, "message": msg, "data": {"listeners": listeners}}

    def full_audit(self) -> dict:
        """Run all audits and return a combined report."""
        results = {
            "startup": self.audit_startup(),
            "tasks": self.audit_scheduled_tasks(),
            "privacy": self.audit_privacy_settings(),
            "network": self.audit_network_listeners(),
        }
        parts = ["Digital Footprint Audit:"]
        for section, r in results.items():
            first_line = r["message"].split("\n")[0]
            parts.append(f"• {section.title()}: {first_line}")
        return {"success": True, "message": "\n".join(parts), "data": results}
