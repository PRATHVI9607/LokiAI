"""
System monitor — CPU, RAM, GPU, disk stats with alerting.
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

try:
    import subprocess
    GPU_AVAILABLE = True
except Exception:
    GPU_AVAILABLE = False


class SystemMonitor:
    """Real-time system resource monitoring."""

    def __init__(self, config: dict):
        self._alert_cpu = config.get("alert_cpu_percent", 90)
        self._alert_ram = config.get("alert_ram_percent", 85)

    def get_stats(self) -> Dict[str, Any]:
        if not PSUTIL_AVAILABLE:
            return {"success": False, "message": "psutil not available. Install with: pip install psutil"}

        stats = {}

        # CPU
        cpu_percent = psutil.cpu_percent(interval=0.5)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        stats["cpu"] = {
            "percent": cpu_percent,
            "cores": cpu_count,
            "freq_mhz": round(cpu_freq.current, 0) if cpu_freq else None,
        }

        # RAM
        mem = psutil.virtual_memory()
        stats["ram"] = {
            "percent": mem.percent,
            "used_gb": round(mem.used / (1024**3), 2),
            "total_gb": round(mem.total / (1024**3), 2),
            "available_gb": round(mem.available / (1024**3), 2),
        }

        # Disk
        try:
            disk = psutil.disk_usage("/")
            stats["disk"] = {
                "percent": disk.percent,
                "used_gb": round(disk.used / (1024**3), 1),
                "total_gb": round(disk.total / (1024**3), 1),
                "free_gb": round(disk.free / (1024**3), 1),
            }
        except Exception:
            stats["disk"] = None

        # GPU (via nvidia-smi)
        stats["gpu"] = self._get_gpu_stats()

        # Network
        net = psutil.net_io_counters()
        stats["network"] = {
            "bytes_sent_mb": round(net.bytes_sent / (1024**2), 1),
            "bytes_recv_mb": round(net.bytes_recv / (1024**2), 1),
        }

        # Format message
        lines = ["System Status:"]
        lines.append(f"  CPU: {cpu_percent}% ({cpu_count} cores)")
        lines.append(f"  RAM: {mem.percent}% ({stats['ram']['used_gb']}GB / {stats['ram']['total_gb']}GB)")

        if stats["disk"]:
            d = stats["disk"]
            lines.append(f"  Disk: {d['percent']}% ({d['used_gb']}GB / {d['total_gb']}GB)")

        if stats["gpu"]:
            g = stats["gpu"]
            lines.append(f"  GPU: {g.get('name', 'GPU')} — {g.get('utilization', '?')}% util, {g.get('memory_used', '?')}MB VRAM")

        # Alerts
        alerts = []
        if cpu_percent >= self._alert_cpu:
            alerts.append(f"⚠ CPU at {cpu_percent}% — critical!")
        if mem.percent >= self._alert_ram:
            alerts.append(f"⚠ RAM at {mem.percent}% — critical!")
        if alerts:
            lines.extend(alerts)

        return {"success": True, "message": "\n".join(lines), "data": stats}

    def _get_gpu_stats(self) -> Dict[str, Any]:
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,utilization.gpu,memory.used,memory.total,temperature.gpu",
                 "--format=csv,noheader,nounits"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                parts = [p.strip() for p in result.stdout.strip().split(",")]
                if len(parts) >= 5:
                    return {
                        "name": parts[0],
                        "utilization": parts[1],
                        "memory_used": parts[2],
                        "memory_total": parts[3],
                        "temperature": parts[4],
                    }
        except Exception:
            pass
        return {}

    def get_top_processes(self, n: int = 10) -> List[Dict]:
        if not PSUTIL_AVAILABLE:
            return []
        procs = []
        for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
            try:
                procs.append(proc.info)
            except Exception:
                pass
        return sorted(procs, key=lambda x: x.get("cpu_percent", 0), reverse=True)[:n]
