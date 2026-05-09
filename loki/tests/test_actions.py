import pytest
from pathlib import Path
from unittest.mock import MagicMock
from loki.actions.file_ops import FileOps
from loki.actions.shell_exec import ShellExec


@pytest.fixture
def file_ops(tmp_path):
    undo = MagicMock()
    return FileOps({"home_dir": str(tmp_path)}, undo)


@pytest.fixture
def shell_exec(tmp_path):
    cfg = {
        "home_dir": str(tmp_path),
        "allowlist_path": None,
    }
    return ShellExec(cfg)


class TestFileOps:
    def test_create_file(self, file_ops, tmp_path):
        result = file_ops.create_file(str(tmp_path / "new.txt"), "content")
        assert result["success"] is True
        assert (tmp_path / "new.txt").read_text() == "content"

    def test_create_file_outside_home_blocked(self, file_ops):
        result = file_ops.create_file("C:\\Windows\\evil.txt", "x")
        assert result["success"] is False

    def test_delete_file(self, file_ops, tmp_path):
        f = tmp_path / "del.txt"
        f.write_text("bye")
        result = file_ops.delete_file(str(f))
        assert result["success"] is True
        assert not f.exists()

    def test_move_file(self, file_ops, tmp_path):
        src = tmp_path / "src.txt"
        src.write_text("data")
        dst = tmp_path / "dst.txt"
        result = file_ops.move(str(src), str(dst))
        assert result["success"] is True
        assert dst.exists()
        assert not src.exists()


class TestShellExec:
    def test_blocked_pattern_rm_rf(self, shell_exec):
        result = shell_exec.execute("rm -rf /")
        assert result["success"] is False
        assert "blocked" in result["message"].lower()

    def test_blocked_pattern_format(self, shell_exec):
        result = shell_exec.execute("format c:")
        assert result["success"] is False

    def test_allowed_echo(self, shell_exec):
        result = shell_exec.execute("echo hello")
        assert result["success"] is True
        assert "hello" in result["data"]
