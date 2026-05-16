import pytest
from fastapi.testclient import TestClient

from src.finpay_sandbox.api import app


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        test_client.post('/test/reset')
        yield test_client
