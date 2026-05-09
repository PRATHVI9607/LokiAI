"""
Natural language file search — find files by name, content, type, date.
"""

import os
import re
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

CONTENT_EXTENSIONS = {".txt", ".md", ".py", ".js", ".ts", ".html", ".css",
                       ".json", ".yaml", ".yml", ".xml", ".csv", ".log", ".ini", ".cfg"}


class FileSearch:
    """Search files using natural language queries."""

    def __init__(self, config: dict):
        self._max_results = config.get("max_results", 20)
        self._search_content = config.get("search_content", True)
        self._max_size_mb = config.get("max_file_size_mb", 10)
        self._home = Path.home()

    def search(self, query: str, directory: Optional[str] = None,
               file_type: Optional[str] = None) -> Dict[str, Any]:
        if not query:
            return {"success": False, "message": "No search query provided."}

        search_dir = Path(directory).expanduser() if directory else self._home
        if not search_dir.exists():
            return {"success": False, "message": f"Directory '{search_dir}' not found."}

        # Parse query for filters
        filters = self._parse_query(query)
        if file_type:
            filters["extensions"] = [f".{file_type.lstrip('.')}"]

        results = self._scan(search_dir, filters, query)
        results.sort(key=lambda x: x["score"], reverse=True)
        results = results[:self._max_results]

        if not results:
            return {"success": True, "message": f"No files found matching '{query}'.", "data": []}

        lines = [f"Found {len(results)} file(s) matching '{query}':"]
        for r in results:
            lines.append(f"  • {r['path']} ({r['size']})")

        return {"success": True, "message": "\n".join(lines), "data": results}

    def _parse_query(self, query: str) -> Dict:
        q = query.lower()
        filters: Dict[str, Any] = {"keywords": [], "extensions": [], "recent_days": None}

        # Date filters
        if "today" in q or "last hour" in q:
            filters["recent_days"] = 0
        elif "yesterday" in q:
            filters["recent_days"] = 1
        elif "last week" in q or "this week" in q:
            filters["recent_days"] = 7
        elif "last month" in q or "this month" in q:
            filters["recent_days"] = 30

        # Extension filters
        ext_map = {
            "pdf": [".pdf"], "image": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
            "video": [".mp4", ".avi", ".mkv", ".mov"], "audio": [".mp3", ".wav", ".flac"],
            "python": [".py"], "javascript": [".js", ".ts"], "code": [".py", ".js", ".ts", ".java", ".cpp"],
            "document": [".doc", ".docx", ".txt", ".md"], "spreadsheet": [".xlsx", ".xls", ".csv"],
            "zip": [".zip", ".rar", ".7z", ".tar", ".gz"],
        }
        for kw, exts in ext_map.items():
            if kw in q:
                filters["extensions"].extend(exts)

        # Keywords from query (remove stop words)
        stop = {"the", "a", "an", "file", "files", "find", "search", "with", "containing",
                "that", "i", "my", "edited", "created", "modified", "show", "me", "all"}
        words = re.findall(r'\b\w{3,}\b', query.lower())
        filters["keywords"] = [w for w in words if w not in stop]

        return filters

    def _scan(self, directory: Path, filters: Dict, original_query: str) -> List[Dict]:
        results = []
        cutoff = None
        if filters["recent_days"] is not None:
            cutoff = datetime.now() - timedelta(days=filters["recent_days"] + 1)

        try:
            for root, dirs, files in os.walk(directory):
                # Skip hidden and system directories
                dirs[:] = [d for d in dirs if not d.startswith(".") and d not in
                           {"__pycache__", "node_modules", ".git", "venv", ".venv"}]

                for fname in files:
                    fpath = Path(root) / fname
                    score = self._score_file(fpath, fname, filters, cutoff, original_query)
                    if score > 0:
                        try:
                            stat = fpath.stat()
                            size_bytes = stat.st_size
                            size_str = self._fmt_size(size_bytes)
                            results.append({
                                "path": str(fpath),
                                "name": fname,
                                "size": size_str,
                                "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
                                "score": score,
                            })
                        except OSError:
                            pass

                if len(results) >= self._max_results * 3:
                    break
        except PermissionError:
            pass

        return results

    def _score_file(self, path: Path, name: str, filters: Dict,
                    cutoff: Optional[datetime], query: str) -> float:
        score = 0.0
        name_lower = name.lower()

        if filters["extensions"] and path.suffix.lower() not in filters["extensions"]:
            return 0.0

        if cutoff:
            try:
                mtime = datetime.fromtimestamp(path.stat().st_mtime)
                if mtime < cutoff:
                    return 0.0
                score += 5.0
            except OSError:
                pass

        for kw in filters["keywords"]:
            if kw in name_lower:
                score += 3.0

        if self._search_content and path.suffix in CONTENT_EXTENSIONS:
            try:
                if path.stat().st_size <= self._max_size_mb * 1024 * 1024:
                    content = path.read_text(encoding="utf-8", errors="ignore").lower()
                    for kw in filters["keywords"]:
                        if kw in content:
                            score += 1.5
            except Exception:
                pass

        return score

    @staticmethod
    def _fmt_size(size: int) -> str:
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size //= 1024
        return f"{size} TB"
