import atexit
import os
import shutil
import tempfile
from pathlib import Path

import pytest

# Cada corrida de pruebas usa su propia base.
_dir = tempfile.mkdtemp(prefix="ordenes-pruebas-")
atexit.register(shutil.rmtree, _dir, ignore_errors=True)
os.environ["ORDENES_BD"] = str(Path(_dir) / "pruebas.db")

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


@pytest.fixture
def cliente_http():
    return TestClient(app)
