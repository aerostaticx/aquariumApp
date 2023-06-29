import pytest
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from mysite import create_app

@pytest.fixture()
def app():
    app = create_app()
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()

def test_addTemperature(client):
    response = client.post('https://aerostatic.pythonanywhere.com/', headers={ 'Content-Type' : 'application/json'}, json={'mcuID' : 'testID', 'temperature' : 88})
    assert "Successfully added temperature." in response.text and response.status_code == 201

def test_getTemperature(client):
    response = client.get('https://aerostatic.pythonanywhere.com/')
    assert "<h1>Temperature Data</h1>" in response.text and response.status_code == 200

# def test_clearTemperature(client):
#     with client.session_transaction() as session:
#             session['username'] = "testID"
#     print(session)
#     response = client.post('https://aerostatic.pythonanywhere.com/clearTemperature')
#     assert "Successfully cleared" in response.text

def test_getProbeStatus(client):
    response = client.post('https://aerostatic.pythonanywhere.com/getProbeStatus', headers={ 'Content-Type' : 'application/json'}, json={'mcuID' : 'testID'})
    assert response.status_code == 200 and "Probe status" in response.text

# def test_initiateProbe(client):
#     response = client.post('https://aerostatic.pythonanywhere.com/initiateProbe')
#     assert response.status_code == 200 and "Probe enabled" in response.text
