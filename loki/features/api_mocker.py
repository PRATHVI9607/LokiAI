"""
ApiMocker — generate mock REST API server code from a plain-English description.
"""

import logging
from pathlib import Path
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from loki.core.brain import LokiBrain

logger = logging.getLogger(__name__)


class ApiMocker:
    def __init__(self, brain: Optional["LokiBrain"] = None):
        self._brain = brain

    def _ask(self, prompt: str) -> str:
        if not self._brain:
            return ""
        return "".join(self._brain.ask(prompt))

    def generate_mock(self, description: str, framework: str = "fastapi",
                      output_path: Optional[str] = None) -> dict:
        """Generate a mock API server from a description."""
        if not description.strip():
            return {"success": False, "message": "Describe the API you want to mock."}

        framework = framework.lower()
        fw_map = {
            "fastapi": "Python FastAPI with uvicorn",
            "express": "Node.js Express.js",
            "flask": "Python Flask",
        }
        fw_desc = fw_map.get(framework, fw_map["fastapi"])

        prompt = (
            f"Generate a complete, runnable {fw_desc} mock API server for the following description:\n\n"
            f"{description}\n\n"
            f"Requirements:\n"
            f"- Include realistic sample/mock data as in-memory dicts or lists\n"
            f"- Implement GET, POST, PUT, DELETE where appropriate\n"
            f"- Add CORS headers for local development\n"
            f"- Include comments explaining each endpoint\n"
            f"- The server should run on port 8080\n"
            f"Return only the complete code file, no extra explanation."
        )
        code = self._ask(prompt).strip()
        if not code:
            return {"success": False, "message": "Could not generate mock API."}

        # Strip markdown code fences if present
        if code.startswith("```"):
            lines = code.split("\n")
            code = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])

        # Save to file if path provided
        if output_path:
            try:
                p = Path(output_path).expanduser().resolve()
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(code, encoding="utf-8")
                return {
                    "success": True,
                    "message": f"Mock API written to {p}. Run it to start the server.",
                    "data": {"path": str(p), "framework": framework, "code": code},
                }
            except Exception as e:
                return {"success": False, "message": f"Could not save file: {e}"}

        return {
            "success": True,
            "message": f"Mock API generated ({framework}):\n\n{code[:500]}{'...' if len(code) > 500 else ''}",
            "data": {"framework": framework, "code": code},
        }

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
