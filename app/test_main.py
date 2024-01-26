from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_welcome():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Reverse Polish Notation calculator!"}


def test_get_ok():
    response = client.get("/rpn?input_str=1_3_%2B")
    assert response.status_code == 200
    assert response.content == b'4'


def test_get_invalid():
    response = client.get("/rpn")
    assert response.status_code == 422


def test_post_ok():
    response = client.post("/rpn/", data=b'"1 1 +"')

    assert response.status_code == 200
    assert response.content == b'2'


def test_post_invalid():
    response = client.post("/rpn/", data=b'"1 1 1"')
    assert response.status_code == 422
    assert response.json() == {'detail': 'Could not process value', 'body': '1 1 1'} 


def test_zero_div():
    response = client.post("/rpn/", data=b'"1 0 /"')
    assert response.status_code == 422
    assert response.json() == {'detail': 'Could not process value', 'body': '1 0 /'} 