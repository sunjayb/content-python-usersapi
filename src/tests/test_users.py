import json
from src.api.models import User

def test_add_user(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/users',
        data=json.dumps({
            'username': 'scully',
            'email': 'dscully@example.com',
            'fullname': 'Dana Scully'
        }),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert 'scully was added!' in data['message']

def test_add_user_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/users',
        data=json.dumps({}),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' in data['message']

def test_add_user_duplicate_email(test_app, test_database):
    client = test_app.test_client()
    client.post(
        '/users',
        data=json.dumps({
            'username': 'scully',
            'email': 'dscully@example.com',
            'fullname': 'Dana Scully'
        }),
        content_type='application/json',
    )
    resp = client.post(
        '/users',
        data=json.dumps({
            'username': 'scully2',
            'email': 'dscully@example.com',
            'fullname': 'Dana Scully'
        }),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Sorry, that email already exists.' in data['message']

def test_add_user_duplicate_username (test_app, test_database):
    client = test_app.test_client()
    client.post(
        '/users',
        data=json.dumps({
            'username': 'scully',
            'email': 'dscully@example.com',
            'fullname': 'Dana Scully'
        }),
        content_type='application/json',
    )
    resp = client.post(
        '/users',
        data=json.dumps({
            'username': 'scully',
            'email': 'dscully2@example.com',
            'fullname': 'Dana Scully'
        }),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Sorry, that username already exists.' in data['message']

def test_get_user(test_app, test_database, add_user):
    user = add_user('scully', 'dscully@example.com', 'Dana Scully')
    client = test_app.test_client()
    resp = client.get(f'/users/{user.id}')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 'scully' in data['username']
    assert 'dscully@example.com' in data['email']
    assert 'Dana Scully' in data['fullname']


def test_get_user_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.get('/users/555')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert 'User 555 does not exist' in data['message']

def test_list_users(test_app, test_database, add_user):
    test_database.session.query(User).delete()
    add_user('scully', 'dscully@example.com', 'Dana Scully')
    add_user('mulder', 'fmulder@example.com', 'Fox Mulder')
    client = test_app.test_client()
    resp = client.get('/users')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 2
    assert 'scully' in data[0]['username']
    assert 'dscully@example.com' in data[0]['email']
    assert 'Dana Scully' in data[0]['fullname']
    assert 'mulder' in data[1]['username']
    assert 'fmulder@example.com' in data[1]['email']
    assert 'Fox Mulder' in data[1]['fullname']
