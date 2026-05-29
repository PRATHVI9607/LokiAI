"""
Process manager — list and kill processes safely.

Kill by name requires an EXACT case-insensitive match.
If no exact match, returns candidate list so the user can pick the right one —
prevents accidental broad kills from substring matching.
"""

import logging
from typing import Dict, Any, List, Union

logger = logging.getLogger(__name__)

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

PROTECTED_PROCESSES = {
    "system", "smss.exe", "csrss.exe", "wininit.exe", "services.exe",
    "lsass.exe", "winlogon.exe", "svchost.exe", "dwm.exe", "explorer.exe",
    "loki.exe", "python.exe", "pythonw.exe",
}


class ProcessManager:
    """List and terminate processes with safety guards."""

    def list_processes(self, top_n: int = 15) -> Dict[str, Any]:
        if not PSUTIL_AVAILABLE:
            return {"success": False, "message": "psutil not available."}

        procs = []
        for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent", "status"]):
            try:
                procs.append({
                    "pid": p.info["pid"],
                    "name": p.info["name"],
                    "cpu": round(p.info.get("cpu_percent", 0) or 0, 1),
                    "mem": round(p.info.get("memory_percent", 0) or 0, 1),
                    "status": p.info.get("status", ""),
                })
            except Exception:
                pass

        procs.sort(key=lambda x: x["cpu"], reverse=True)
        top = procs[:top_n]
        lines = [f"Top {len(top)} processes by CPU:"]
        for p in top:
            lines.append(f"  [{p['pid']}] {p['name']} — CPU: {p['cpu']}% | RAM: {p['mem']}%")
        return {"success": True, "message": "\n".join(lines), "data": top}

    def kill(self, name_or_pid: Union[str, int, None]) -> Dict[str, Any]:
        if not PSUTIL_AVAILABLE:
            return {"success": False, "message": "psutil not available."}
        if not name_or_pid:
            return {"success": False, "message": "Specify an exact process name or PID."}

        # ── Kill by PID ──────────────────────────────────────────────────
        if isinstance(name_or_pid, int) or (isinstance(name_or_pid, str) and str(name_or_pid).isdigit()):
            pid = int(name_or_pid)
            try:
                proc = psutil.Process(pid)
                pname = proc.name()
                if pname.lower() in PROTECTED_PROCESSES:
                    return {"success": False, "message": f"'{pname}' is a protected process — cannot kill."}
                proc.terminate()
                return {"success": True, "message": f"Terminated: {pname} (PID {pid})."}
            except psutil.NoSuchProcess:
                return {"success": False, "message": f"No process with PID {pid}."}
            except psutil.AccessDenied:
                return {"success": False, "message": f"Access denied to PID {pid}. Run Loki as administrator."}
            except Exception as e:
                return {"success": False, "message": f"Kill failed: {e}"}

        # ── Kill by exact name ────────────────────────────────────────────
        target = str(name_or_pid).lower().strip()
        exact_matches: list = []
        substring_candidates: List[Dict] = []

        for proc in psutil.process_iter(["pid", "name"]):
            try:
                pname = proc.info["name"]
                pname_lc = pname.lower()
                if pname_lc == target:
                    exact_matches.append(proc)
                elif target in pname_lc:
                    substring_candidates.append({"pid": proc.info["pid"], "name": pname})
            except Exception:
                pass

        if not exact_matches:
            if substring_candidates:
                lines = [f"No exact match for '{name_or_pid}'. Candidates:"]
                for c in substring_candidates[:8]:
                    lines.append(f"  [{c['pid']}] {c['name']}")
                lines.append("Retry with exact name or PID.")
                return {
                    "success": False,
                    "message": "\n".join(lines),
                    "data": {"candidates": substring_candidates},
                }
            return {"success": False, "message": f"No process named '{name_or_pid}' found."}

        killed, errors = [], []
        for proc in exact_matches:
            try:
                pname = proc.info["name"]
                pid = proc.info["pid"]
                if pname.lower() in PROTECTED_PROCESSES:
                    errors.append(f"'{pname}' is protected — skipped.")
                    continue
                proc.terminate()
                killed.append(f"{pname} (PID {pid})")
            except psutil.AccessDenied:
                errors.append(f"Access denied to PID {proc.info['pid']}.")
            except Exception as e:
                errors.append(str(e))

        parts = []
        if killed:
            parts.append(f"Terminated: {', '.join(killed)}.")
        if errors:
            parts.append(" ".join(errors))
        return {"success": bool(killed), "message": " ".join(parts) or "Nothing killed."}
