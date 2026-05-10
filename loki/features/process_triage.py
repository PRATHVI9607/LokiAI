"""
ProcessTriage — identify and optionally terminate resource-heavy background processes
to free RAM/CPU when launching a demanding application.
"""

import logging
from typing import Optional

import psutil

logger = logging.getLogger(__name__)

# Processes known to be safe to suspend/kill for resource recovery
SAFE_TO_KILL = {
    "teams.exe", "slack.exe", "discord.exe", "spotify.exe", "onedrive.exe",
    "dropbox.exe", "googledrivesync.exe", "steam.exe", "epicgameslauncher.exe",
    "origin.exe", "skype.exe", "zoom.exe", "obs64.exe", "obs32.exe",
    "greenshot.exe", "sharex.exe", "notion.exe", "figma.exe",
}

PROTECTED = {
    "system", "smss.exe", "csrss.exe", "wininit.exe", "winlogon.exe",
    "lsass.exe", "services.exe", "svchost.exe", "explorer.exe",
    "dwm.exe", "fontdrvhost.exe", "registry", "memory compression",
}


class ProcessTriage:
    def _snapshot(self) -> list[dict]:
        procs = []
        for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_info", "status"]):
            try:
                info = p.info
                name = (info.get("name") or "").lower()
                if name in PROTECTED:
                    continue
                mem_mb = round((info.get("memory_info") or psutil.virtual_memory()).rss / 1048576, 1)
                procs.append({
                    "pid": info["pid"],
                    "name": info["name"],
                    "cpu": info.get("cpu_percent", 0) or 0,
                    "mem_mb": mem_mb,
                    "safe": name in SAFE_TO_KILL,
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return procs

    def analyze(self, top_n: int = 10) -> dict:
        """Show top resource consumers and flag safe-to-kill candidates."""
        procs = self._snapshot()
        procs.sort(key=lambda p: p["mem_mb"], reverse=True)
        top = procs[:top_n]
        safe_candidates = [p for p in top if p["safe"]]
        total_safe_mb = round(sum(p["mem_mb"] for p in safe_candidates), 1)

        lines = [f"  {p['name']} — {p['mem_mb']} MB RAM{'  ← safe to close' if p['safe'] else ''}" for p in top]
        msg = f"Top {len(top)} processes by RAM:\n" + "\n".join(lines)
        if safe_candidates:
            msg += f"\n\n{len(safe_candidates)} non-essential processes using ~{total_safe_mb} MB could be closed."
        return {
            "success": True,
            "message": msg,
            "data": {"top": top, "safe_candidates": safe_candidates, "reclaimable_mb": total_safe_mb},
        }

    def triage_for_app(self, app_name: str, dry_run: bool = True) -> dict:
        """Kill safe non-essential processes to free resources for app_name."""
        procs = self._snapshot()
        safe = [p for p in procs if p["safe"]]
        if not safe:
            return {"success": True, "message": "No non-essential processes to close.", "data": {"killed": []}}

        killed = []
        errors = []
        for p in safe:
            if dry_run:
                killed.append(p["name"])
                continue
            try:
                proc = psutil.Process(p["pid"])
                proc.terminate()
                killed.append(p["name"])
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                errors.append(f"{p['name']}: {e}")

        freed_mb = round(sum(p["mem_mb"] for p in safe if p["name"] in killed), 1)
        verb = "Would close" if dry_run else "Closed"
        msg = f"{verb} {len(killed)} processes, freeing ~{freed_mb} MB for {app_name}."
        if errors:
            msg += f"\n  Errors: {'; '.join(errors[:3])}"
        return {
            "success": True,
            "message": msg,
            "data": {"killed": killed, "freed_mb": freed_mb, "dry_run": dry_run, "errors": errors},
        }

    def suspend_process(self, name_or_pid: str) -> dict:
        """Suspend (pause) a process by name or PID."""
        target = None
        try:
            pid = int(name_or_pid)
            target = psutil.Process(pid)
        except ValueError:
            for p in psutil.process_iter(["pid", "name"]):
                try:
                    if name_or_pid.lower() in (p.info.get("name") or "").lower():
                        target = p
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

        if not target:
            return {"success": False, "message": f"Process '{name_or_pid}' not found."}

        try:
            name = target.name()
            if name.lower() in PROTECTED:
                return {"success": False, "message": f"Cannot suspend protected process: {name}"}
            target.suspend()
            return {"success": True, "message": f"Suspended {name} (PID {target.pid}).", "data": {"pid": target.pid}}
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            return {"success": False, "message": str(e)}

    def resume_process(self, name_or_pid: str) -> dict:
        """Resume a previously suspended process."""
        target: Optional[psutil.Process] = None
        try:
            pid = int(name_or_pid)
            target = psutil.Process(pid)
        except ValueError:
            for p in psutil.process_iter(["pid", "name"]):
                try:
                    if name_or_pid.lower() in (p.info.get("name") or "").lower():
                        target = p
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

        if not target:
            return {"success": False, "message": f"Process '{name_or_pid}' not found."}

        try:
            target.resume()
            return {"success": True, "message": f"Resumed {target.name()} (PID {target.pid}).", "data": {"pid": target.pid}}
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            return {"success": False, "message": str(e)}
