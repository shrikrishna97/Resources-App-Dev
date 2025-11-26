from app import app
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client
        
def test_index(client):
    response = client.get('/')
    print(response.status_code)
    assert response.status_code == 200
    assert b'Hello, World!' in response.data  
    
    
def test_about(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b'This is the about page.' in response.data

def test_greet(client):
    response = client.get('/greet/Alice')
    assert response.status_code == 200
    assert b'Hello, Alice!' in response.data          