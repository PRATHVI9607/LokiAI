"""
GoogleIntegration — real Gmail + Google Calendar access.

"What's on my calendar today?", "any new email?", "what's my next meeting?"

ONE-TIME SETUP (required to activate — Loki can't do this for you):
  1. Go to https://console.cloud.google.com → create a project
  2. Enable the Gmail API and Google Calendar API
  3. Create OAuth client credentials (Desktop app), download as
     loki/credentials/google_credentials.json
  4. First use opens a browser to authorize; the token is cached at
     loki/credentials/google_token.json — you only do this once.

Until that's done every method returns a friendly "not set up yet" message
with these steps, so nothing crashes.
"""

import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]

_SETUP_MSG = (
    "Google isn't connected yet. One-time setup: create a Google Cloud project, "
    "enable the Gmail + Calendar APIs, download OAuth Desktop credentials to "
    "loki/credentials/google_credentials.json, then ask me again — I'll open the "
    "consent screen once."
)


class GoogleIntegration:
    def __init__(self, memory_dir: Path):
        self._dir = Path(memory_dir).parent / "credentials"
        self._creds_file = self._dir / "google_credentials.json"
        self._token_file = self._dir / "google_token.json"
        self._service_cal = None
        self._service_gmail = None
        self._available = self._creds_file.exists()
        if not self._available:
            logger.info("Google integration not configured (no credentials) — optional")

    # ── auth ─────────────────────────────────────────────────────────────

    def _ensure(self) -> bool:
        """Build/refresh credentials and the API services. Returns True if ready."""
        if self._service_cal and self._service_gmail:
            return True
        if not self._creds_file.exists():
            return False
        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build

            creds = None
            if self._token_file.exists():
                creds = Credentials.from_authorized_user_file(str(self._token_file), SCOPES)
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(str(self._creds_file), SCOPES)
                    creds = flow.run_local_server(port=0)
                self._dir.mkdir(parents=True, exist_ok=True)
                self._token_file.write_text(creds.to_json(), encoding="utf-8")
            self._service_cal = build("calendar", "v3", credentials=creds, cache_discovery=False)
            self._service_gmail = build("gmail", "v1", credentials=creds, cache_discovery=False)
            return True
        except Exception as e:
            logger.error(f"Google auth failed: {e}")
            return False

    # ── calendar ─────────────────────────────────────────────────────────

    def upcoming_events(self, days: int = 1) -> Dict[str, Any]:
        if not self._ensure():
            return {"success": False, "message": _SETUP_MSG}
        try:
            now = datetime.now(timezone.utc)
            end = now + timedelta(days=days)
            res = self._service_cal.events().list(
                calendarId="primary", timeMin=now.isoformat(), timeMax=end.isoformat(),
                singleEvents=True, orderBy="startTime", maxResults=15,
            ).execute()
            events = res.get("items", [])
            if not events:
                return {"success": True, "message": f"Nothing on your calendar in the next {days} day(s)."}
            lines = []
            for e in events:
                start = e["start"].get("dateTime", e["start"].get("date", ""))
                when = start[11:16] if "T" in start else "all day"
                lines.append(f"  • {when} — {e.get('summary', '(untitled)')}")
            return {"success": True,
                    "message": f"You have {len(events)} event(s):\n" + "\n".join(lines),
                    "data": {"events": events}}
        except Exception as e:
            return {"success": False, "message": f"Calendar read failed: {e}"}

    def next_meeting(self) -> Dict[str, Any]:
        r = self.upcoming_events(days=7)
        if not r.get("success") or not r.get("data", {}).get("events"):
            return r if not r.get("success") else {"success": True, "message": "No upcoming meetings this week."}
        e = r["data"]["events"][0]
        start = e["start"].get("dateTime", e["start"].get("date", ""))
        return {"success": True, "message": f"Next up: {e.get('summary', '(untitled)')} at {start[:16].replace('T', ' ')}."}

    # ── gmail ────────────────────────────────────────────────────────────

    def unread_summary(self, count: int = 5) -> Dict[str, Any]:
        if not self._ensure():
            return {"success": False, "message": _SETUP_MSG}
        try:
            res = self._service_gmail.users().messages().list(
                userId="me", labelIds=["UNREAD", "INBOX"], maxResults=count,
            ).execute()
            msgs = res.get("messages", [])
            if not msgs:
                return {"success": True, "message": "Inbox zero — no unread mail."}
            lines = []
            for m in msgs:
                full = self._service_gmail.users().messages().get(
                    userId="me", id=m["id"], format="metadata",
                    metadataHeaders=["From", "Subject"],
                ).execute()
                hdrs = {h["name"]: h["value"] for h in full.get("payload", {}).get("headers", [])}
                sender = hdrs.get("From", "?").split("<")[0].strip().strip('"')
                lines.append(f"  • {sender}: {hdrs.get('Subject', '(no subject)')[:60]}")
            return {"success": True,
                    "message": f"{len(msgs)} unread:\n" + "\n".join(lines),
                    "data": {"count": len(msgs)}}
        except Exception as e:
            return {"success": False, "message": f"Gmail read failed: {e}"}

    def send_email(self, to: str, subject: str, body: str) -> Dict[str, Any]:
        if not self._ensure():
            return {"success": False, "message": _SETUP_MSG}
        if not to:
            return {"success": False, "message": "Who should I send it to?"}
        try:
            import base64
            from email.mime.text import MIMEText
            msg = MIMEText(body or "")
            msg["to"] = to
            msg["subject"] = subject or "(no subject)"
            raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
            self._service_gmail.users().messages().send(
                userId="me", body={"raw": raw},
            ).execute()
            return {"success": True, "message": f"Sent to {to}."}
        except Exception as e:
            return {"success": False, "message": f"Send failed: {e}"}

    def create_event(self, title: str, start_iso: str, duration_minutes: int = 60) -> Dict[str, Any]:
        if not self._ensure():
            return {"success": False, "message": _SETUP_MSG}
        if not title or not start_iso:
            return {"success": False, "message": "I need a title and a start time."}
        try:
            start = datetime.fromisoformat(start_iso)
            end = start + timedelta(minutes=duration_minutes)
            event = {
                "summary": title,
                "start": {"dateTime": start.isoformat()},
                "end": {"dateTime": end.isoformat()},
            }
            created = self._service_cal.events().insert(calendarId="primary", body=event).execute()
            when = start.strftime("%a %d %b %H:%M")
            return {"success": True, "message": f"Added '{title}' on {when}.",
                    "data": {"link": created.get("htmlLink")}}
        except ValueError:
            return {"success": False, "message": f"Couldn't parse the start time '{start_iso}' (use ISO like 2026-06-01T15:00)."}
        except Exception as e:
            return {"success": False, "message": f"Couldn't create the event: {e}"}

    @property
    def is_available(self) -> bool:
        return self._creds_file.exists()
