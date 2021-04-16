def test_register_valid_data_status_code(app, client):
    post_data = {
        'username': 'username test',
        'email': 'test@mail.ru',
        'password': 'test2021',
    }
    response = client.post('/register/', json=post_data)
    assert response.status_code == 201


def test_register_invalid_data_status_code(app, client):
    post_data = {
        'username': 'username test',
        'email': 'test@mail.ru',
    }
    response = client.post('/register/', json=post_data)
    assert response.status_code == 400


def test_login_valid_data_status_code(app, client):
    post_data = {
        'email': 'test@mail.ru',
        'password': 'test2021',
    }
    response = client.post('/login/', json=post_data)
    assert response.status_code == 200


def test_login_invalid_data_status_code(app, client):
    post_data = {
        'email': 'test@mail.ru',
        'password': 'test20',
    }
    response = client.post('/login/', json=post_data)
    assert response.status_code == 401