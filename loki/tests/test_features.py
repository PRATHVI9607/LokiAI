import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from loki.features.task_manager import TaskManager
from loki.features.clipboard_manager import ClipboardManager
from loki.features.security_scanner import SecurityScanner
from loki.features.file_organizer import FileOrganizer
from loki.features.vault import Vault


@pytest.fixture
def memory_mgr(tmp_path):
    from loki.core.memory import MemoryManager
    return MemoryManager(tmp_path / "memory")


@pytest.fixture
def task_mgr(memory_mgr):
    return TaskManager(memory_mgr)


class TestTaskManager:
    def test_add_and_list(self, task_mgr):
        task_mgr.add("write tests", priority="high")
        result = task_mgr.list_tasks()
        assert result["success"] is True
        assert any("write tests" in t["title"] for t in result["data"])

    def test_priority_sorting(self, task_mgr):
        task_mgr.add("low task", priority="low")
        task_mgr.add("high task", priority="high")
        result = task_mgr.list_tasks()
        titles = [t["title"] for t in result["data"]]
        assert titles.index("high task") < titles.index("low task")

    def test_complete_task(self, task_mgr):
        task_mgr.add("deploy loki", priority="medium")
        tasks = task_mgr.list_tasks()["data"]
        tid = tasks[0]["id"]
        result = task_mgr.complete(tid)
        assert result["success"] is True

    def test_delete_task(self, task_mgr):
        task_mgr.add("delete me")
        tid = task_mgr.list_tasks()["data"][0]["id"]
        result = task_mgr.delete(tid)
        assert result["success"] is True
        assert task_mgr.list_tasks()["data"] == []

    def test_empty_title_rejected(self, task_mgr):
        result = task_mgr.add("")
        assert result["success"] is False


class TestClipboardManager:
    def test_history_tracks_entries(self):
        cm = ClipboardManager()
        cm._history.append("entry one")
        cm._history.append("entry two")
        result = cm.get_history()
        assert result["success"] is True
        assert "entry two" in result["data"]

    def test_get_item_copies_to_clipboard(self):
        cm = ClipboardManager()
        cm._history.append("restore me")
        with patch("pyperclip.copy") as mock_copy:
            result = cm.get_item(0)
            mock_copy.assert_called_once_with("restore me")
        assert result["success"] is True

    def test_clear(self):
        cm = ClipboardManager()
        cm._history.extend(["a", "b", "c"])
        result = cm.clear()
        assert result["success"] is True
        assert cm._history == []

    def test_get_item_out_of_range(self):
        cm = ClipboardManager()
        result = cm.get_item(99)
        assert result["success"] is False


class TestSecurityScanner:
    def test_detects_openai_key(self, tmp_path):
        f = tmp_path / "config.py"
        f.write_text('API_KEY = "sk-' + 'a' * 48 + '"')
        scanner = SecurityScanner()
        result = scanner.scan(str(tmp_path))
        assert result["success"] is True
        assert len(result["data"]) > 0

    def test_detects_aws_key(self, tmp_path):
        f = tmp_path / "creds.py"
        f.write_text('aws_key = "AKIAIOSFODNN7EXAMPLE"')
        scanner = SecurityScanner()
        result = scanner.scan(str(tmp_path))
        assert result["success"] is True
        assert any(r["type"] == "AWS Access Key" for r in result["data"])

    def test_clean_file_no_findings(self, tmp_path):
        f = tmp_path / "clean.py"
        f.write_text("def hello():\n    return 42\n")
        scanner = SecurityScanner()
        result = scanner.scan(str(tmp_path))
        assert result["success"] is True
        assert len(result["data"]) == 0


class TestFileOrganizer:
    def test_organizes_image(self, tmp_path):
        img = tmp_path / "photo.jpg"
        img.write_bytes(b"\xff\xd8\xff")
        organizer = FileOrganizer({})
        result = organizer.organize(str(tmp_path))
        assert result["success"] is True
        assert (tmp_path / "Images" / "photo.jpg").exists()

    def test_organizes_document(self, tmp_path):
        doc = tmp_path / "report.pdf"
        doc.write_bytes(b"%PDF")
        organizer = FileOrganizer({})
        result = organizer.organize(str(tmp_path))
        assert (tmp_path / "Documents" / "report.pdf").exists()

    def test_empty_directory(self, tmp_path):
        organizer = FileOrganizer({})
        result = organizer.organize(str(tmp_path))
        assert result["success"] is True
        assert "already organized" in result["message"].lower()


class TestVault:
    def test_set_and_get(self, tmp_path):
        v = Vault(tmp_path / "vault.dat")
        v.unlock("testpassword")
        result_store = v.store("key1", "secret_value")
        assert result_store["success"] is True
        result_get = v.retrieve("key1")
        assert result_get["success"] is True
        assert result_get["data"] == "secret_value"

    def test_get_missing_key(self, tmp_path):
        v = Vault(tmp_path / "vault.dat")
        v.unlock("testpassword")
        result = v.retrieve("nonexistent")
        assert result["success"] is False

    def test_locked_vault_rejects_ops(self, tmp_path):
        v = Vault(tmp_path / "vault.dat")
        # not unlocked
        assert v.store("k", "v")["success"] is False
        assert v.retrieve("k")["success"] is False

    def test_wrong_password_fails(self, tmp_path):
        vault_path = tmp_path / "vault.dat"
        v1 = Vault(vault_path)
        v1.unlock("correct")
        v1.store("k", "v")

        v2 = Vault(vault_path)
        result = v2.unlock("wrong")
        assert result["success"] is False

    def test_list_and_delete_keys(self, tmp_path):
        v = Vault(tmp_path / "vault.dat")
        v.unlock("pw")
        v.store("alpha", "1")
        v.store("beta", "2")
        keys = v.list_keys()
        assert "alpha" in keys["data"]
        del_result = v.delete("alpha")
        assert del_result["success"] is True
        assert "alpha" not in v.list_keys()["data"]
