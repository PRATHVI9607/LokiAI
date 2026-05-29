"""
EnvSetup — generate Docker, virtual environment, and dependency configuration for projects.
Preview-first: generators return content without writing. Call save_*() to persist.
"""

import logging
from pathlib import Path
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from loki.core.brain import LokiBrain

logger = logging.getLogger(__name__)


class EnvSetup:
    def __init__(self, brain: Optional["LokiBrain"] = None):
        self._brain = brain

    def _ask(self, prompt: str) -> str:
        if not self._brain:
            return ""
        return "".join(self._brain.ask(prompt))

    def _read_project_files(self, project_path: Path) -> str:
        """Read key project files to understand the stack."""
        snippets = []
        key_files = [
            "requirements.txt", "pyproject.toml", "setup.py", "package.json",
            "go.mod", "Cargo.toml", "pom.xml", "build.gradle",
        ]
        for fname in key_files:
            fp = project_path / fname
            if fp.exists():
                try:
                    content = fp.read_text(encoding="utf-8", errors="replace")[:800]
                    snippets.append(f"--- {fname} ---\n{content}")
                except Exception:
                    pass
        return "\n\n".join(snippets) or "No dependency files found."

    def generate_dockerfile(self, project_path: str = ".") -> dict:
        """Generate a production-ready Dockerfile preview. Does NOT write automatically."""
        p = Path(project_path).expanduser().resolve()
        if not p.exists():
            return {"success": False, "message": f"Project path not found: {project_path}"}

        project_info = self._read_project_files(p)
        prompt = (
            f"Generate a production-ready, multi-stage Dockerfile for a project with these files:\n\n"
            f"{project_info}\n\n"
            f"Include: .dockerignore entries as a comment, health check, non-root user, "
            f"minimal base image, correct port exposure. Return only the Dockerfile content."
        )
        dockerfile = self._ask(prompt).strip()
        if not dockerfile:
            return {"success": False, "message": "Could not generate Dockerfile."}

        out = p / "Dockerfile"
        preview = dockerfile[:1500] + ("\n... (truncated)" if len(dockerfile) > 1500 else "")
        return {
            "success": True,
            "message": f"Dockerfile preview (review and say 'save it' to write to {out}):\n\n{preview}",
            "data": {"path": str(out), "content": dockerfile, "pending_write": True},
        }

    def save_dockerfile(self, project_path: str, content: str) -> dict:
        """Write a previously generated Dockerfile to disk."""
        p = Path(project_path).expanduser().resolve()
        out = p / "Dockerfile"
        try:
            out.write_text(content, encoding="utf-8")
            return {"success": True, "message": f"Dockerfile written to {out}", "data": {"path": str(out)}}
        except Exception as e:
            return {"success": False, "message": f"Could not write Dockerfile: {e}"}

    def generate_venv_script(self, project_path: str = ".", python: str = "python") -> dict:
        """Generate a PowerShell venv setup script preview. Does NOT write automatically."""
        p = Path(project_path).expanduser().resolve()
        project_info = self._read_project_files(p)

        prompt = (
            f"Generate a Windows PowerShell setup script that:\n"
            f"1. Creates a Python venv using '{python}'\n"
            f"2. Activates it\n"
            f"3. Upgrades pip\n"
            f"4. Installs dependencies based on:\n{project_info}\n"
            f"5. Prints success message\n"
            f"Return only the PowerShell script."
        )
        script = self._ask(prompt).strip()
        if not script:
            return {"success": False, "message": "Could not generate venv setup script."}

        out = p / "setup_env.ps1"
        preview = script[:1500] + ("\n... (truncated)" if len(script) > 1500 else "")
        return {
            "success": True,
            "message": f"setup_env.ps1 preview (say 'save it' to write to {out}):\n\n{preview}",
            "data": {"path": str(out), "content": script, "pending_write": True},
        }

    def save_venv_script(self, project_path: str, content: str) -> dict:
        """Write a previously generated venv script to disk."""
        out = Path(project_path).expanduser().resolve() / "setup_env.ps1"
        try:
            out.write_text(content, encoding="utf-8")
            return {"success": True, "message": f"Setup script written to {out}. Run: .\\setup_env.ps1", "data": {"path": str(out)}}
        except Exception as e:
            return {"success": False, "message": f"Could not write script: {e}"}

    def generate_docker_compose(self, project_path: str = ".", services: str = "") -> dict:
        """Generate a docker-compose.yml preview. Does NOT write automatically."""
        p = Path(project_path).expanduser().resolve()
        project_info = self._read_project_files(p)

        prompt = (
            f"Generate a docker-compose.yml for a project with these dependencies:\n{project_info}\n"
            + (f"Additional services needed: {services}\n" if services else "")
            + "Include volumes, environment variables, healthchecks, and restart policies. "
            "Return only the YAML content."
        )
        compose = self._ask(prompt).strip()
        if not compose:
            return {"success": False, "message": "Could not generate docker-compose.yml."}

        out = p / "docker-compose.yml"
        preview = compose[:1500] + ("\n... (truncated)" if len(compose) > 1500 else "")
        return {
            "success": True,
            "message": f"docker-compose.yml preview (say 'save it' to write to {out}):\n\n{preview}",
            "data": {"path": str(out), "content": compose, "pending_write": True},
        }

    def save_docker_compose(self, project_path: str, content: str) -> dict:
        """Write a previously generated docker-compose.yml to disk."""
        out = Path(project_path).expanduser().resolve() / "docker-compose.yml"
        try:
            out.write_text(content, encoding="utf-8")
            return {"success": True, "message": f"docker-compose.yml written to {out}", "data": {"path": str(out)}}
        except Exception as e:
            return {"success": False, "message": f"Could not write file: {e}"}
