from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..main import app
from ..routers.queries import get_session
from ..sqla.db import Base, SQLALCHEMY_DATABASE_URL


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_session():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_session] = override_get_session

client = TestClient(app)


def test_export():
    response = client.post(
        "/query/",
        data=b'"1 1 +"',
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["result"] == 2

    response = client.get("/query?input_str=1_3_%2B")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["result"] == 4

    response = client.get("/export/")
    assert response.status_code == 200, response.text
    data = response.content
    assert data == b'input,result\n1 1 +,2.0\n1 3 +,4.0\n'



def test_welcome():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the Reverse Polish Notation calculator!"
    }


def test_get_ok():
    response = client.get("/query?input_str=1_3_%2B")
    assert response.status_code == 200
    assert response.content == b'{"input":"1 3 +","result":4}'


def test_get_invalid():
    response = client.get("/query")
    assert response.status_code == 422


def test_post_ok():
    response = client.post("/query/", data=b'"1 1 +"')

    assert response.status_code == 200
    assert response.content == b'{"input":"1 1 +","result":2}'


def test_post_invalid():
    response = client.post("/query/", data=b'"1 1 1"')
    assert response.status_code == 422
    assert response.json() == {"detail": "Could not process value", "body": "1 1 1"}


def test_zero_div():
    response = client.post("/query/", data=b'"1 0 /"')
    assert response.status_code == 422
    assert response.json() == {"detail": "Could not process value", "body": "1 0 /"}
