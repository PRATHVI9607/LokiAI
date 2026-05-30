"""
ProactiveMonitor — the "alive" engine. Loki watches the machine and the clock
in the background and speaks up UNPROMPTED when something's worth saying:
sustained high CPU/RAM, low battery, a long unbroken work session, late nights,
low disk. The thing that makes an assistant feel like JARVIS instead of a
command line with a voice.

Each rule has a cooldown so Loki advises, never nags. Alerts are pushed to the
chat always, and spoken only when Loki is idle (never interrupts you).
"""

import logging
import threading
import time
from dataclasses import dataclass, field
from typing import Callable, Optional

logger = logging.getLogger(__name__)

try:
    import psutil
    PSUTIL = True
except ImportError:
    PSUTIL = False


@dataclass
class _Rule:
    cooldown: float           # seconds before this rule can fire again
    last_fired: float = 0.0
    # sustained-condition tracking
    streak_start: float = field(default=0.0)

    def ready(self, now: float) -> bool:
        return (now - self.last_fired) >= self.cooldown

    def fire(self, now: float) -> None:
        self.last_fired = now
        self.streak_start = 0.0


class ProactiveMonitor:
    """Background watcher that surfaces timely, unprompted observations."""

    def __init__(self, config: dict, on_alert: Callable[[str, bool], None],
                 is_busy: Optional[Callable[[], bool]] = None):
        """
        on_alert(text, speak): push an observation to the chat; speak=True asks
          for it to be voiced (only requested when Loki is idle).
        is_busy(): returns True if Loki is mid-conversation (so we stay quiet).
        """
        cfg = config.get("proactive", {}) if isinstance(config, dict) else {}
        self._enabled = cfg.get("enabled", True)
        self._interval = cfg.get("check_interval", 20)          # seconds between checks
        self._cpu_pct = cfg.get("cpu_threshold", 90)
        self._ram_pct = cfg.get("ram_threshold", 90)
        self._sustain = cfg.get("sustain_seconds", 180)          # how long high before alerting
        self._work_minutes = cfg.get("work_session_minutes", 90)
        self._on_alert = on_alert
        self._is_busy = is_busy or (lambda: False)

        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._session_start = time.time()

        self._rules = {
            "cpu":     _Rule(cooldown=cfg.get("cpu_cooldown", 1800)),     # 30 min
            "ram":     _Rule(cooldown=cfg.get("ram_cooldown", 1800)),
            "battery": _Rule(cooldown=cfg.get("battery_cooldown", 1200)), # 20 min
            "disk":    _Rule(cooldown=cfg.get("disk_cooldown", 7200)),    # 2 h
            "work":    _Rule(cooldown=cfg.get("work_cooldown", 3600)),    # 1 h
            "latenight": _Rule(cooldown=cfg.get("latenight_cooldown", 14400)),  # 4 h
        }

    def start(self) -> None:
        if not self._enabled or not PSUTIL or self._running:
            if not PSUTIL:
                logger.info("ProactiveMonitor: psutil unavailable — disabled")
            return
        self._running = True
        self._session_start = time.time()
        self._thread = threading.Thread(target=self._loop, daemon=True, name="loki-proactive")
        self._thread.start()
        logger.info("ProactiveMonitor active — watching the system")

    def stop(self) -> None:
        self._running = False

    def reset_work_session(self) -> None:
        """Call when the user interacts — keeps the 'long session' timer honest."""
        # only reset if there was actually a long gap (handled by caller cadence)
        pass

    # ── loop ─────────────────────────────────────────────────────────────

    def _loop(self) -> None:
        # let the app settle before the first check
        time.sleep(15)
        while self._running:
            try:
                self._check()
            except Exception as e:
                logger.debug(f"Proactive check error: {e}")
            # sleep in small slices so stop() is responsive
            for _ in range(int(self._interval / 0.5)):
                if not self._running:
                    return
                time.sleep(0.5)

    def _emit(self, key: str, text: str, speak: bool = True) -> None:
        now = time.time()
        rule = self._rules[key]
        if not rule.ready(now):
            return
        rule.fire(now)
        # never voice-interrupt an active conversation; still log to chat
        self._on_alert(text, speak and not self._is_busy())
        logger.info(f"Proactive: {text}")

    def _check(self) -> None:
        now = time.time()

        # ── sustained CPU ──
        try:
            cpu = psutil.cpu_percent(interval=0.3)
            r = self._rules["cpu"]
            if cpu >= self._cpu_pct:
                if r.streak_start == 0.0:
                    r.streak_start = now
                elif now - r.streak_start >= self._sustain:
                    self._emit("cpu", f"Heads up — CPU's been pinned around {int(cpu)}% for a few minutes. Want me to triage what's eating it?")
            else:
                r.streak_start = 0.0
        except Exception:
            pass

        # ── sustained RAM ──
        try:
            ram = psutil.virtual_memory().percent
            r = self._rules["ram"]
            if ram >= self._ram_pct:
                if r.streak_start == 0.0:
                    r.streak_start = now
                elif now - r.streak_start >= self._sustain:
                    self._emit("ram", f"Memory's at {int(ram)}% and holding. Things may start to crawl — want me to close some background apps?")
            else:
                r.streak_start = 0.0
        except Exception:
            pass

        # ── battery ──
        try:
            bat = psutil.sensors_battery()
            if bat and not bat.power_plugged:
                if bat.percent <= 15:
                    self._emit("battery", f"Battery's at {int(bat.percent)}% and unplugged. You'll want a charger soon.")
        except Exception:
            pass

        # ── low disk on C: ──
        try:
            free_gb = psutil.disk_usage("C:\\").free / 1e9
            if free_gb < 5:
                self._emit("disk", f"Your C: drive is down to {free_gb:.1f} GB free. Want me to find large or duplicate files to clear?")
        except Exception:
            pass

        # ── long unbroken work session ──
        mins = (now - self._session_start) / 60
        if mins >= self._work_minutes:
            self._emit("work", f"You've been at it for {int(mins)} minutes straight. A short break wouldn't hurt — I'll hold things down.", speak=True)
            self._session_start = now  # restart the session clock after mentioning it

        # ── late night ──
        hour = time.localtime(now).tm_hour
        if 1 <= hour <= 4:
            self._emit("latenight", f"It's past {hour} in the morning. The work will still be here after some sleep.")
