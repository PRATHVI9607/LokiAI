"""
CalendarManager — parse local .ics calendar files, detect scheduling conflicts,
and suggest alternative meeting times via LLM.
"""

import logging
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from loki.core.brain import LokiBrain

logger = logging.getLogger(__name__)

# Windows Calendar / Outlook common ICS export locations
DEFAULT_ICS_DIRS = [
    Path.home() / "AppData/Local/Microsoft/Outlook",
    Path.home() / "AppData/Roaming/Microsoft/Outlook",
    Path.home() / "Documents/Calendars",
    Path.home() / "OneDrive",
]


def _parse_dt(value: str) -> Optional[datetime]:
    """Parse iCalendar datetime strings."""
    value = value.split(";")[-1].replace("Z", "").strip()
    for fmt in ("%Y%m%dT%H%M%S", "%Y%m%dT%H%M", "%Y%m%d"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    return None


def _parse_ics(ics_text: str) -> list[dict]:
    """Parse an ICS text into a list of event dicts."""
    events = []
    current: Optional[dict] = None
    in_valarm = False

    for raw_line in ics_text.splitlines():
        line = raw_line.strip()
        if line == "BEGIN:VEVENT":
            current = {}
            in_valarm = False
        elif line == "BEGIN:VALARM":
            in_valarm = True
        elif line == "END:VALARM":
            in_valarm = False
        elif line == "END:VEVENT" and current is not None:
            if current.get("start"):
                events.append(current)
            current = None
        elif current is not None and not in_valarm and ":" in line:
            key, _, val = line.partition(":")
            key = key.split(";")[0].upper()
            val = val.replace("\\n", "\n").replace("\\,", ",").strip()
            if key == "DTSTART":
                current["start"] = _parse_dt(val)
            elif key == "DTEND":
                current["end"] = _parse_dt(val)
            elif key == "SUMMARY":
                current["title"] = val
            elif key == "DESCRIPTION":
                current["description"] = val[:200]
            elif key == "LOCATION":
                current["location"] = val

    return events


def _find_ics_files() -> list[Path]:
    files = []
    for d in DEFAULT_ICS_DIRS:
        if d.exists():
            files.extend(d.rglob("*.ics"))
    return files[:10]


class CalendarManager:
    def __init__(self, brain: Optional["LokiBrain"] = None, ics_path: Optional[str] = None):
        self._brain = brain
        self._ics_path = Path(ics_path).expanduser().resolve() if ics_path else None

    def _llm(self, prompt: str) -> str:
        if not self._brain:
            return ""
        return "".join(self._brain.ask(prompt))

    def _load_events(self, ics_path: Optional[Path] = None) -> tuple[list[dict], str]:
        """Load events from an ICS file. Returns (events, source_path)."""
        path = ics_path or self._ics_path
        if path and path.exists():
            text = path.read_text(encoding="utf-8", errors="replace")
            return _parse_ics(text), str(path)

        # Auto-discover
        files = _find_ics_files()
        if not files:
            return [], ""
        text = files[0].read_text(encoding="utf-8", errors="replace")
        return _parse_ics(text), str(files[0])

    def list_events(self, days: int = 7, ics_path: Optional[str] = None) -> dict:
        """List calendar events in the next N days."""
        fp = Path(ics_path).expanduser().resolve() if ics_path else None
        events, source = self._load_events(fp)
        if not events:
            return {
                "success": False,
                "message": "No calendar file found. Provide an .ics file path or export from Outlook/Google Calendar.",
            }

        now = datetime.now()
        cutoff = now + timedelta(days=days)
        upcoming = [
            e for e in events
            if e.get("start") and now <= e["start"] <= cutoff
        ]
        upcoming.sort(key=lambda e: e["start"])

        if not upcoming:
            return {"success": True, "message": f"No events in the next {days} days.", "data": {"events": []}}

        lines = []
        for e in upcoming:
            start_str = e["start"].strftime("%a %b %d, %I:%M %p")
            end_str = e["end"].strftime("%I:%M %p") if e.get("end") else "?"
            lines.append(f"  {start_str} – {end_str}: {e.get('title', 'Untitled')}")

        msg = f"{len(upcoming)} event(s) in next {days} days (from {Path(source).name}):\n" + "\n".join(lines)
        return {"success": True, "message": msg, "data": {"events": upcoming, "source": source}}

    def find_conflicts(self, ics_path: Optional[str] = None) -> dict:
        """Detect overlapping calendar events."""
        fp = Path(ics_path).expanduser().resolve() if ics_path else None
        events, source = self._load_events(fp)
        if not events:
            return {"success": False, "message": "No calendar file found."}

        now = datetime.now()
        future = [e for e in events if e.get("start") and e["start"] >= now and e.get("end")]
        future.sort(key=lambda e: e["start"])

        conflicts = []
        for i in range(len(future)):
            for j in range(i + 1, len(future)):
                a, b = future[i], future[j]
                if b["start"] >= a["end"]:
                    break
                if a["start"] < b["end"] and b["start"] < a["end"]:
                    conflicts.append({"event_a": a, "event_b": b})

        if not conflicts:
            return {"success": True, "message": "No scheduling conflicts found.", "data": {"conflicts": []}}

        lines = []
        for c in conflicts[:10]:
            a, b = c["event_a"], c["event_b"]
            lines.append(
                f"  CONFLICT: '{a.get('title', '?')}' ({a['start'].strftime('%H:%M')}–{a['end'].strftime('%H:%M')}) "
                f"↔ '{b.get('title', '?')}' ({b['start'].strftime('%H:%M')}–{b['end'].strftime('%H:%M')}) "
                f"on {a['start'].strftime('%b %d')}"
            )

        msg = f"Found {len(conflicts)} scheduling conflict(s):\n" + "\n".join(lines)
        return {"success": True, "message": msg, "data": {"conflicts": conflicts}}

    def suggest_alternatives(self, event_title: str, duration_minutes: int = 60,
                              ics_path: Optional[str] = None) -> dict:
        """Suggest free time slots for a meeting given existing calendar."""
        fp = Path(ics_path).expanduser().resolve() if ics_path else None
        events, _ = self._load_events(fp)

        now = datetime.now().replace(minute=0, second=0, microsecond=0)
        # Consider next 5 business days, 9am–6pm
        busy_slots = []
        for e in events:
            if e.get("start") and e.get("end") and e["start"] >= now:
                busy_slots.append((e["start"], e["end"]))

        free_slots = []
        day = now
        for _ in range(7):
            day += timedelta(days=1)
            if day.weekday() >= 5:  # skip weekends
                continue
            work_start = day.replace(hour=9, minute=0)
            work_end = day.replace(hour=18, minute=0)
            cursor = work_start
            while cursor + timedelta(minutes=duration_minutes) <= work_end:
                slot_end = cursor + timedelta(minutes=duration_minutes)
                overlap = any(s < slot_end and cursor < e for s, e in busy_slots)
                if not overlap:
                    free_slots.append(cursor)
                cursor += timedelta(minutes=30)
            if len(free_slots) >= 5:
                break

        if not free_slots:
            return {"success": True, "message": "No free slots found in the next 7 business days.", "data": {"slots": []}}

        slot_strs = [s.strftime("%A %b %d, %I:%M %p") for s in free_slots[:5]]

        if self._brain:
            prompt = (
                f"A meeting '{event_title}' ({duration_minutes} min) needs scheduling. "
                f"Available slots:\n" + "\n".join(f"  {s}" for s in slot_strs) +
                "\n\nWhich slot would you recommend and why? Keep it brief."
            )
            recommendation = self._llm(prompt)
        else:
            recommendation = ""

        msg = f"Free slots for '{event_title}' ({duration_minutes} min):\n"
        msg += "\n".join(f"  {i+1}. {s}" for i, s in enumerate(slot_strs))
        if recommendation:
            msg += f"\n\nRecommendation: {recommendation}"

        return {
            "success": True,
            "message": msg,
            "data": {"slots": [s.isoformat() for s in free_slots[:5]], "recommendation": recommendation},
        }

    def import_ics(self, ics_path: str) -> dict:
        """Load and validate an ICS file, returning event count."""
        fp = Path(ics_path).expanduser().resolve()
        if not fp.exists():
            return {"success": False, "message": f"File not found: {fp}"}
        if fp.suffix.lower() != ".ics":
            return {"success": False, "message": "Expected an .ics file."}
        self._ics_path = fp
        events, _ = self._load_events(fp)
        return {
            "success": True,
            "message": f"Loaded {len(events)} events from {fp.name}.",
            "data": {"count": len(events), "path": str(fp)},
        }
