import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    r = client.get('/')
    assert r.status_code == 200

def test_health(client):
    r = client.get('/health')
    assert r.status_code == 200
    assert r.get_json()['status'] == 'OK'

def test_error_endpoint(client):
    r = client.get('/error')
    assert r.status_code == 500