import pytest
import tempfile
import shutil
from pathlib import Path


@pytest.fixture(scope="session")
def tmp_home(tmp_path_factory):
    home = tmp_path_factory.mktemp("home")
    yield home
    shutil.rmtree(home, ignore_errors=True)


@pytest.fixture
def tmp_dir(tmp_path):
    return tmp_path


@pytest.fixture
def sample_text_file(tmp_path):
    f = tmp_path / "sample.txt"
    f.write_text("Hello from Loki test suite.")
    return f


@pytest.fixture
def sample_py_file(tmp_path):
    f = tmp_path / "sample.py"
    f.write_text('import os\nprint("hello")\n')
    return f
