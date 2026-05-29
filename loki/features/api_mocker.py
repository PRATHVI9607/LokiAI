"""
ApiMocker — generate mock REST API server code from a plain-English description.
Preview-first: generated code is returned without writing automatically.
Call save_mock() to persist after reviewing.
"""

import logging
import os
from pathlib import Path
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from loki.core.brain import LokiBrain

logger = logging.getLogger(__name__)

_HOME = Path(os.path.expanduser("~")).resolve()


class ApiMocker:
    def __init__(self, brain: Optional["LokiBrain"] = None):
        self._brain = brain

    def _ask(self, prompt: str) -> str:
        if not self._brain:
            return ""
        return "".join(self._brain.ask(prompt))

    def _strip_fences(self, code: str) -> str:
        if code.startswith("```"):
            lines = code.split("\n")
            return "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
        return code

    def generate_mock(self, description: str, framework: str = "fastapi") -> dict:
        """Generate a mock API server preview. Does NOT write automatically."""
        if not description.strip():
            return {"success": False, "message": "Describe the API you want to mock."}

        framework = framework.lower()
        fw_map = {
            "fastapi": "Python FastAPI with uvicorn",
            "express": "Node.js Express.js",
            "flask": "Python Flask",
        }
        fw_desc = fw_map.get(framework, fw_map["fastapi"])
        ext_map = {"fastapi": "py", "flask": "py", "express": "js"}
        ext = ext_map.get(framework, "py")

        prompt = (
            f"Generate a complete, runnable {fw_desc} mock API server for:\n\n"
            f"{description}\n\n"
            f"Requirements:\n"
            f"- Include realistic in-memory sample data\n"
            f"- Implement GET, POST, PUT, DELETE where appropriate\n"
            f"- Add CORS headers for local development\n"
            f"- Include brief comments on each endpoint\n"
            f"- Run on port 8080\n"
            f"Return only the complete code file."
        )
        code = self._strip_fences(self._ask(prompt).strip())
        if not code:
            return {"success": False, "message": "Could not generate mock API."}

        suggested_name = f"mock_api.{ext}"
        preview = code[:800] + ("\n... (truncated)" if len(code) > 800 else "")
        return {
            "success": True,
            "message": (
                f"Mock API preview ({framework}) — say 'save it' to write to ~/{suggested_name}:\n\n{preview}"
            ),
            "data": {
                "framework": framework,
                "code": code,
                "suggested_name": suggested_name,
                "pending_write": True,
            },
        }

    def save_mock(self, code: str, filename: str = "mock_api.py") -> dict:
        """Write a previously generated mock API to the home directory."""
        # Restrict writes to home directory
        dest = (_HOME / filename).resolve()
        if not dest.is_relative_to(_HOME):
            return {"success": False, "message": "Write destination must be inside your home directory."}
        try:
            dest.write_text(code, encoding="utf-8")
            return {
                "success": True,
                "message": f"Mock API written to {dest}. Start it with: python {dest.name}",
                "data": {"path": str(dest)},
            }
        except Exception as e:
            return {"success": False, "message": f"Could not save file: {e}"}

    def generate_mock_data(self, schema: str, count: int = 10) -> dict:
        """Generate mock JSON data matching a schema description."""
        if not schema.strip():
            return {"success": False, "message": "Describe the data schema."}
        prompt = (
            f"Generate {count} realistic mock JSON objects matching this schema: {schema}.\n"
            f"Return a valid JSON array only, no explanation."
        )
        result = self._ask(prompt).strip()
        if not result:
            return {"success": False, "message": "Could not generate mock data."}
        return {"success": True, "message": f"Generated {count} mock records.", "data": {"json": result}}
