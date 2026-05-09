import pytest
from unittest.mock import MagicMock, patch
from loki.features.task_manager import TaskManager
from loki.features.clipboard_manager import ClipboardManager
from loki.features.security_scanner import SecurityScanner
from loki.features.file_organizer import FileOrganizer
from loki.features.vault import Vault


@pytest.fixture
def memory_mgr(tmp_path):
    from loki.core.memory import MemoryManager
    with patch("loki.core.memory.MEMORY_DIR", tmp_path):
        return MemoryManager({})


@pytest.fixture
def task_mgr(memory_mgr):
    return TaskManager({}, memory_mgr)


class TestTaskManager:
    def test_add_and_list(self, task_mgr):
        task_mgr.add_task("write tests", priority="high")
        result = task_mgr.list_tasks()
        assert result["success"] is True
        assert any("write tests" in t["text"] for t in result["data"])

    def test_complete_task(self, task_mgr):
        task_mgr.add_task("deploy loki", priority="medium")
        tasks = task_mgr.list_tasks()["data"]
        tid = tasks[0]["id"]
        result = task_mgr.complete_task(tid)
        assert result["success"] is True


class TestClipboardManager:
    def test_history_tracks_entries(self):
        cm = ClipboardManager({})
        cm._history.append("entry one")
        cm._history.append("entry two")
        result = cm.get_history()
        assert result["success"] is True
        assert "entry two" in result["data"]

    def test_restore(self):
        cm = ClipboardManager({})
        cm._history.append("restore me")
        with patch("pyperclip.copy") as mock_copy:
            result = cm.restore(0)
            mock_copy.assert_called_once_with("restore me")
        assert result["success"] is True


class TestSecurityScanner:
    def test_detects_api_key(self, tmp_path):
        f = tmp_path / "config.py"
        f.write_text('API_KEY = "sk-abc123def456ghi789jkl012mno345pqr"')
        scanner = SecurityScanner({"home_dir": str(tmp_path)})
        result = scanner.scan(str(tmp_path))
        assert result["success"] is True
        assert len(result["data"]) > 0

    def test_clean_file_no_findings(self, tmp_path):
        f = tmp_path / "clean.py"
        f.write_text("def hello():\n    return 42\n")
        scanner = SecurityScanner({"home_dir": str(tmp_path)})
        result = scanner.scan(str(tmp_path))
        assert result["success"] is True
        assert len(result["data"]) == 0


class TestFileOrganizer:
    def test_organizes_image(self, tmp_path):
        img = tmp_path / "photo.jpg"
        img.write_bytes(b"\xff\xd8\xff")
        organizer = FileOrganizer({"home_dir": str(tmp_path)})
        result = organizer.organize(str(tmp_path))
        assert result["success"] is True
        assert (tmp_path / "Images" / "photo.jpg").exists()


class TestVault:
    def test_set_and_get(self, tmp_path):
        v = Vault({"vault_path": str(tmp_path / "vault.dat")})
        v.unlock("testpassword")
        v.set("key1", "secret_value")
        result = v.get("key1")
        assert result["success"] is True
        assert result["data"] == "secret_value"

    def test_get_missing_key(self, tmp_path):
        v = Vault({"vault_path": str(tmp_path / "vault.dat")})
        v.unlock("testpassword")
        result = v.get("nonexistent")
        assert result["success"] is False

    def test_wrong_password_fails(self, tmp_path):
        vault_path = str(tmp_path / "vault.dat")
        v1 = Vault({"vault_path": vault_path})
        v1.unlock("correct")
        v1.set("k", "v")

        v2 = Vault({"vault_path": vault_path})
        result = v2.unlock("wrong")
        assert result["success"] is False
