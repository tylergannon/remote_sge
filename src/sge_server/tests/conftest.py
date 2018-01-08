import pytest
import sge_server

@pytest.fixture
def app():
    sge_server.app.testing = True
    return sge_server.app

@pytest.fixture
def client(app):
    return app.test_client()
