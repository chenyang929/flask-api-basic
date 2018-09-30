import pytest
from app import create_app
from app.models.mongo import mongo
import json


@pytest.fixture
def client():
    app = create_app()
    client = app.test_client()
    yield client
    # 清理数据库
    mongo.db.user.delete_many({})


data = {"account": "1234567@qq.com", "nickname": "1234567", "secret": "1234567", "type": 100}


def register(client):
    rv = client.post('v1/client/register', json=data)
    return rv


def test_register(client):
    rv = register(client)
    assert b'ok' in rv.data


def test_get_token(client):
    test_register(client)
    rv = client.post('v1/token', json=data)
    assert '201' in rv.status


def test_verify_token(client):
    test_register(client)
    rv = client.post('v1/token', json=data)
    token = json.loads(rv.data.decode('utf-8'))
    rv = client.post('v1/token/secret', json=token)
    assert b'scope' in rv.data


def test_hello(client):
    rv = client.get('v1/user/test')
    assert b'ok' in rv.data



