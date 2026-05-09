"""
Process manager — list and kill processes safely.
"""

import logging
from typing import Dict, Any, List, Union

logger = logging.getLogger(__name__)

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

# Protect critical system processes
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
            return {"success": False, "message": "Specify a process name or PID."}

        killed = []
        errors = []

        if isinstance(name_or_pid, int) or (isinstance(name_or_pid, str) and name_or_pid.isdigit()):
            pid = int(name_or_pid)
            try:
                proc = psutil.Process(pid)
                if proc.name().lower() in PROTECTED_PROCESSES:
                    return {"success": False, "message": f"Process '{proc.name()}' is protected."}
                proc.terminate()
                killed.append(f"{proc.name()} (PID {pid})")
            except psutil.NoSuchProcess:
                return {"success": False, "message": f"No process with PID {pid}."}
            except psutil.AccessDenied:
                return {"success": False, "message": f"Access denied to PID {pid}. Run as administrator."}
        else:
            target = str(name_or_pid).lower()
            for proc in psutil.process_iter(["pid", "name"]):
                try:
                    pname = proc.info["name"].lower()
                    if target in pname:
                        if pname in PROTECTED_PROCESSES:
                            errors.append(f"'{proc.info['name']}' is protected — skipped.")
                            continue
                        proc.terminate()
                        killed.append(f"{proc.info['name']} (PID {proc.info['pid']})")
                except Exception:
                    pass

        if killed:
            return {"success": True, "message": f"Terminated: {', '.join(killed)}."}
        if errors:
            return {"success": False, "message": " ".join(errors)}
        return {"success": False, "message": f"No process matching '{name_or_pid}' found."}
