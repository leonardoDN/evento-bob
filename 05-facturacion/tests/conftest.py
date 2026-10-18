import atexit
import os
import shutil
import tempfile
from pathlib import Path

import pytest

# Cada corrida de pruebas usa su propia base y un PAC que siempre responde rápido.
_dir = tempfile.mkdtemp(prefix="pedidos-pruebas-")
atexit.register(shutil.rmtree, _dir, ignore_errors=True)
os.environ["PEDIDOS_BD"] = str(Path(_dir) / "pruebas.db")
os.environ["PAC_PROB_FALLA"] = "0"
os.environ["PAC_DEMORA_MIN"] = "0"
os.environ["PAC_DEMORA_MAX"] = "0"

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


@pytest.fixture
def cliente_http():
    return TestClient(app)
