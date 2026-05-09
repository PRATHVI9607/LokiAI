import pytest
from unittest.mock import MagicMock
from loki.actions.file_ops import FileOps
from loki.actions.shell_exec import ShellExec


@pytest.fixture
def undo():
    return MagicMock()


@pytest.fixture
def file_ops(undo):
    # FileOps restricts paths to the real home dir; tmp_path is under home on all platforms
    return FileOps(undo)


@pytest.fixture
def shell_exec(undo):
    cfg = {"shell_timeout": 10}
    return ShellExec(cfg, undo)


class TestFileOps:
    def test_create_file(self, file_ops, tmp_path):
        target = tmp_path / "new.txt"
        result = file_ops.create_file(str(target), "content")
        assert result["success"] is True
        assert target.read_text() == "content"

    def test_create_file_already_exists(self, file_ops, tmp_path):
        f = tmp_path / "exists.txt"
        f.write_text("already here")
        result = file_ops.create_file(str(f), "new content")
        assert result["success"] is False

    def test_create_file_outside_home_blocked(self, file_ops):
        # C:\Windows is outside home dir on any normal Windows system
        result = file_ops.create_file("C:\\Windows\\System32\\evil.txt", "x")
        assert result["success"] is False
        assert "denied" in result["message"].lower()

    def test_delete_file(self, file_ops, tmp_path):
        f = tmp_path / "del.txt"
        f.write_text("bye")
        result = file_ops.delete_file(str(f))
        assert result["success"] is True
        assert not f.exists()

    def test_delete_nonexistent_file(self, file_ops, tmp_path):
        result = file_ops.delete_file(str(tmp_path / "ghost.txt"))
        assert result["success"] is False

    def test_move_file(self, file_ops, tmp_path):
        src = tmp_path / "src.txt"
        src.write_text("data")
        dst = tmp_path / "dst.txt"
        result = file_ops.move(str(src), str(dst))
        assert result["success"] is True
        assert dst.exists()
        assert not src.exists()

    def test_create_file_pushes_undo(self, file_ops, undo, tmp_path):
        file_ops.create_file(str(tmp_path / "undo_test.txt"), "")
        undo.push.assert_called_once()


class TestShellExec:
    def test_blocked_rm_rf(self, shell_exec):
        result = shell_exec.execute("rm -rf /")
        assert result["success"] is False
        assert "not permitted" in result["message"].lower()

    def test_blocked_format(self, shell_exec):
        result = shell_exec.execute("format c:")
        assert result["success"] is False

    def test_blocked_shutdown(self, shell_exec):
        result = shell_exec.execute("shutdown -r -t 0")
        assert result["success"] is False

    def test_empty_command(self, shell_exec):
        result = shell_exec.execute("")
        assert result["success"] is False

    def test_allowed_echo(self, shell_exec):
        result = shell_exec.execute("echo hello")
        assert result["success"] is True
        assert "hello" in result.get("message", "") or "hello" in str(result.get("data", ""))
