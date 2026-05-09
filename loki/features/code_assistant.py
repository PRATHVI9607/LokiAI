"""
Code assistant — analyze bugs, generate commit messages, README, regex, SQL.
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from loki.core.brain import LokiBrain

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".cpp", ".c", ".h",
    ".cs", ".go", ".rs", ".rb", ".php", ".swift", ".kt", ".scala"
}


class CodeAssistant:
    """LLM-powered code analysis and generation."""

    MAX_CODE_CHARS = 6000

    def __init__(self, brain: Optional["LokiBrain"] = None):
        self._brain = brain

    def _require_brain(self) -> Optional[Dict]:
        if not self._brain:
            return {"success": False, "message": "LLM brain not available."}
        return None

    def _ask(self, prompt: str) -> str:
        return "".join(self._brain.ask(prompt))

    def analyze(self, path: str) -> Dict[str, Any]:
        err = self._require_brain()
        if err:
            return err

        file_path = Path(path).expanduser().resolve()
        if not file_path.exists():
            return {"success": False, "message": f"File not found: {file_path}"}

        try:
            code = file_path.read_text(encoding="utf-8", errors="replace")[:self.MAX_CODE_CHARS]
        except Exception as e:
            return {"success": False, "message": f"Cannot read file: {e}"}

        prompt = (
            f"Analyze this {file_path.suffix} code for bugs, security issues, and code smells. "
            f"Be specific and concise. List issues with line numbers if possible.\n\n"
            f"File: {file_path.name}\n```{file_path.suffix.lstrip('.')}\n{code}\n```"
        )
        result = self._ask(prompt)
        return {"success": True, "message": result, "data": {"file": str(file_path)}}

    def convert(self, path: str, from_lang: str, to_lang: str) -> Dict[str, Any]:
        err = self._require_brain()
        if err:
            return err

        file_path = Path(path).expanduser().resolve()
        if not file_path.exists():
            return {"success": False, "message": f"File not found: {file_path}"}

        code = file_path.read_text(encoding="utf-8", errors="replace")[:self.MAX_CODE_CHARS]
        prompt = (
            f"Convert the following {from_lang} code to {to_lang}. "
            f"Maintain all logic, add appropriate type hints, and follow {to_lang} idioms.\n\n"
            f"```{from_lang}\n{code}\n```\n\n"
            f"Provide only the converted code, no explanation."
        )
        result = self._ask(prompt)
        return {"success": True, "message": result}

    def generate_readme(self, repo_path: Optional[str] = None) -> Dict[str, Any]:
        err = self._require_brain()
        if err:
            return err

        target = Path(repo_path).expanduser().resolve() if repo_path else Path.cwd()
        if not target.exists():
            return {"success": False, "message": f"Directory not found: {target}"}

        # Gather structure
        structure = []
        for item in sorted(target.iterdir()):
            if item.name.startswith(".") or item.name in {"__pycache__", "node_modules", "venv"}:
                continue
            structure.append(("  " if item.is_file() else "") + item.name + ("/" if item.is_dir() else ""))

        # Read key files if they exist
        context_files = {}
        for fname in ["main.py", "app.py", "index.js", "package.json", "pyproject.toml", "setup.py"]:
            fpath = target / fname
            if fpath.exists():
                try:
                    context_files[fname] = fpath.read_text(encoding="utf-8", errors="replace")[:1500]
                except Exception:
                    pass

        context = "\n".join(f"{k}:\n{v[:500]}" for k, v in context_files.items())
        structure_text = "\n".join(structure[:30])
        prompt = (
            f"Generate a professional README.md for this project. "
            f"Include: title, description, features, installation, usage, and license sections.\n\n"
            f"Project structure:\n{structure_text}\n\nKey files:\n{context}"
        )
        result = self._ask(prompt)
        return {"success": True, "message": result}

    def generate_regex(self, description: str) -> Dict[str, Any]:
        err = self._require_brain()
        if err:
            return err

        prompt = (
            f"Generate a Python regex pattern for: '{description}'. "
            f"Respond with ONLY the regex pattern (no explanation, no code block). "
            f"Test examples if helpful. Pattern only."
        )
        result = self._ask(prompt)
        return {"success": True, "message": f"Regex: {result.strip()}", "data": {"pattern": result.strip()}}

    def build_sql(self, description: str, schema: Optional[str] = None) -> Dict[str, Any]:
        err = self._require_brain()
        if err:
            return err

        schema_text = f"\nSchema:\n{schema}" if schema else ""
        prompt = (
            f"Convert this natural language query to SQL: '{description}'{schema_text}\n\n"
            f"Respond with ONLY the SQL query (no explanation)."
        )
        result = self._ask(prompt)
        return {"success": True, "message": result.strip(), "data": {"query": result.strip()}}
