from ..models import Recipe


def test_get_recipes_status_code(app, client):
    response = client.get('/recipes/')
    assert response.status_code == 200


def test_get_recipes_content_type(app, client):
    response = client.get('/recipes/')
    assert response.headers['Content-Type'] == 'application/json'


def test_get_recipes_content(app, client):
    response = client.get('/recipes/')
    data = response.json
    recipe = Recipe.query.first()
    assert isinstance(data, list) and data[0]['title'] == recipe.title


def test_post_recipe_with_valid_data_status_code(app, client):
    post_data = {
        'title': 'Blog test',
        'short_description': 'Short test',
        'description': 'Short test',
        'category_id': 1,
    }
    response = client.post('/recipes/', json=post_data)
    assert response.status_code == 201


def test_post_recipe_with_valid_data_content(app, client):
    post_data = {
        'title': 'Blog test',
        'short_description': 'Short test',
        'description': 'Short test',
        'category_id': 1,
    }
    response = client.post('/recipes/', json=post_data)
    data = response.json
    assert data.get('id')
    assert data.get('title') and data.get('title') == post_data['title']


def test_post_recipe_with_invalid_status_code(app, client):
    post_data = {
        'short_description': 'Short test',
        'description': 'Short test',
        'category_id': 1,
    }
    response = client.post('/recipes/', json=post_data)
    assert response.status_code == 400


def test_post_recipe_with_invalid_error_message(app, client):
    post_data = {
        'short_description': 'Short test',
        'description': 'Short test',
        'category_id': 1,
    }
    response = client.post('/recipes/', json=post_data)
    assert response.status_code == 400
    assert 'title' in response.json
    assert 'Missing data for required field.' in response.json['title']