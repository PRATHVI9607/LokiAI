"""
Git helper — status, diff, commit message generation, commit execution.
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from loki.core.brain import LokiBrain

logger = logging.getLogger(__name__)

try:
    import git
    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False
    logger.warning("gitpython not available: pip install gitpython")


class GitHelper:
    """Git operations with LLM-powered commit message generation."""

    def __init__(self, brain: Optional["LokiBrain"] = None):
        self._brain = brain

    def _get_repo(self, path: Optional[str] = None):
        search_path = Path(path).expanduser().resolve() if path else Path.cwd()
        try:
            return git.Repo(search_path, search_parent_directories=True)
        except Exception:
            return None

    def get_status(self, repo_path: Optional[str] = None) -> Dict[str, Any]:
        if not GIT_AVAILABLE:
            return {"success": False, "message": "gitpython not installed: pip install gitpython"}

        repo = self._get_repo(repo_path)
        if not repo:
            return {"success": False, "message": "Not in a git repository."}

        try:
            branch = repo.active_branch.name
            changed = [item.a_path for item in repo.index.diff(None)]
            staged = [item.a_path for item in repo.index.diff("HEAD")]
            untracked = repo.untracked_files[:10]

            lines = [f"Repository: {Path(repo.working_dir).name} [{branch}]"]
            if staged:
                lines.append(f"  Staged ({len(staged)}): {', '.join(staged[:5])}")
            if changed:
                lines.append(f"  Modified ({len(changed)}): {', '.join(changed[:5])}")
            if untracked:
                lines.append(f"  Untracked ({len(untracked)}): {', '.join(untracked[:5])}")
            if not staged and not changed and not untracked:
                lines.append("  Working tree clean.")

            return {"success": True, "message": "\n".join(lines)}
        except Exception as e:
            return {"success": False, "message": f"Git status failed: {e}"}

    def generate_commit_message(self, repo_path: Optional[str] = None) -> Dict[str, Any]:
        if not GIT_AVAILABLE:
            return {"success": False, "message": "gitpython not installed."}

        repo = self._get_repo(repo_path)
        if not repo:
            return {"success": False, "message": "Not in a git repository."}

        try:
            diff = repo.git.diff("HEAD", "--stat")
            diff_detail = repo.git.diff("HEAD")[:3000]
        except Exception:
            try:
                diff = repo.git.diff("--cached", "--stat")
                diff_detail = repo.git.diff("--cached")[:3000]
            except Exception as e:
                return {"success": False, "message": f"Cannot get diff: {e}"}

        if not diff.strip():
            return {"success": False, "message": "No changes to commit."}

        if self._brain:
            prompt = (
                f"Generate a concise, conventional git commit message for these changes. "
                f"Format: <type>(<scope>): <description> — max 72 chars. No body.\n\n"
                f"Diff summary:\n{diff}\n\nDetailed diff (truncated):\n{diff_detail}"
            )
            message = "".join(self._brain.ask(prompt)).strip()
            return {"success": True, "message": f"Suggested commit message:\n{message}", "data": {"message": message}}

        return {"success": False, "message": "LLM not available for commit message generation."}

    @staticmethod
    def _remote_kind(url: str) -> str:
        """Classify a remote URL. Both SSH and HTTPS are fully supported — the
        underlying git binary uses the user's SSH keys / credential helper."""
        u = (url or "").strip()
        if u.startswith("git@") or u.startswith("ssh://") or (":" in u and "//" not in u and "@" in u):
            return "ssh"
        if u.startswith(("http://", "https://")):
            return "https"
        return "other"

    def remote_info(self, repo_path: Optional[str] = None) -> Dict[str, Any]:
        if not GIT_AVAILABLE:
            return {"success": False, "message": "gitpython not installed."}
        repo = self._get_repo(repo_path)
        if not repo:
            return {"success": False, "message": "Not in a git repository."}
        try:
            remotes = list(repo.remotes)
            if not remotes:
                return {"success": True, "message": "No remotes configured.", "data": {"remotes": []}}
            lines, data = ["Remotes:"], []
            for r in remotes:
                url = next(iter(r.urls), "")
                kind = self._remote_kind(url)
                lines.append(f"  {r.name} → {url} [{kind}]")
                data.append({"name": r.name, "url": url, "kind": kind})
            return {"success": True, "message": "\n".join(lines), "data": {"remotes": data}}
        except Exception as e:
            return {"success": False, "message": f"Couldn't read remotes: {e}"}

    def pull(self, repo_path: Optional[str] = None) -> Dict[str, Any]:
        if not GIT_AVAILABLE:
            return {"success": False, "message": "gitpython not installed."}
        repo = self._get_repo(repo_path)
        if not repo:
            return {"success": False, "message": "Not in a git repository."}
        if not repo.remotes:
            return {"success": False, "message": "No remote to pull from."}
        try:
            # repo.git.pull delegates to the git binary → SSH keys / credential
            # helpers work exactly as they do on the command line.
            out = repo.git.pull()
            return {"success": True, "message": f"Pulled.\n{out[:300]}" if out else "Already up to date."}
        except Exception as e:
            return {"success": False, "message": f"Pull failed: {e}"}

    def push(self, repo_path: Optional[str] = None) -> Dict[str, Any]:
        if not GIT_AVAILABLE:
            return {"success": False, "message": "gitpython not installed."}
        repo = self._get_repo(repo_path)
        if not repo:
            return {"success": False, "message": "Not in a git repository."}
        if not repo.remotes:
            return {"success": False, "message": "No remote to push to."}
        try:
            branch = repo.active_branch.name
            out = repo.git.push("origin", branch)  # SSH or HTTPS — git handles auth
            return {"success": True, "message": f"Pushed {branch} to origin.\n{out[:300]}".strip()}
        except Exception as e:
            return {"success": False, "message": f"Push failed: {e}"}

    def commit(self, message: str, repo_path: Optional[str] = None) -> Dict[str, Any]:
        if not GIT_AVAILABLE:
            return {"success": False, "message": "gitpython not installed."}
        if not message:
            return {"success": False, "message": "Commit message required."}

        repo = self._get_repo(repo_path)
        if not repo:
            return {"success": False, "message": "Not in a git repository."}

        try:
            # Only commit already-staged changes — never auto-stage with -A which
            # could silently include .env files, credentials, or unintended binaries.
            staged = [item.a_path for item in repo.index.diff("HEAD")]
            if not staged:
                return {
                    "success": False,
                    "message": "No staged changes to commit. Stage files explicitly with 'git add <files>' first.",
                }
            repo.index.commit(message)
            return {
                "success": True,
                "message": f"Committed {len(staged)} file(s): '{message}'",
                "data": {"staged": staged},
            }
        except Exception as e:
            return {"success": False, "message": f"Commit failed: {e}"}
