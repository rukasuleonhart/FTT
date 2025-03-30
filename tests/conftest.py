import pytest
from fastapi.testclient import TestClient
from ftt.app import app  # Certifique-se de importar corretamente sua aplicação

@pytest.fixture
def client():
    return TestClient(app)
