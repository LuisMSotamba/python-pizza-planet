from app.common.decorators import generic_response
from app.common.http_methods import *
import pytest

# Test GET method response with instance
def test_get_method_with_instance(app, client):
    @app.route('/fake-get/')
    @generic_response(GET)
    def fn():
        return {'hello': 'world'}, None
    
    response = client.get('/fake-get/')

    pytest.assume(response.status_code==200)
    pytest.assume(response.json['hello']=='world')

# Test GET method response with error
def test_get_method_with_error(app, client):
    @app.route('/fake-get-error/')
    @generic_response(GET)
    def fn():
        return None, 'Could not find'

    response = client.get('/fake-get-error/')
    pytest.assume(response.status_code == 400)
    pytest.assume(response.json['error']=='Could not find')

# Test POST method response with instance
def test_post_method_with_instance(app, client):
    @app.route('/fake-post/', methods=POST)
    @generic_response(POST)
    def fn():
        return {'id': 1}, None

    response = client.post('/fake-post/')
    pytest.assume(response.status_code==200)
    pytest.assume(response.json['id']==1)

# Test POST method response with error
def test_post_method_with_error(app, client):
    @app.route('/fake-post-error/', methods=POST)
    @generic_response(POST)
    def fn():
        return None, 'Duplicate id'

    response = client.post('/fake-post-error/')
    pytest.assume(response.status_code==400)
    pytest.assume(response.json['error']=='Duplicate id')

# Test PUT method response with instance
def test_put_method_with_instance(app, client):
    @app.route('/fake-put/', methods=PUT)
    @generic_response(PUT)
    def fn():
        return {'message': 'updated successfully'}, None

    response = client.put('/fake-put/')
    pytest.assume(response.status_code==200)
    pytest.assume(response.json['message']=='updated successfully')

# Test PUT method response with error
def test_put_method_with_error(app, client):
    @app.route('/fake-put-error/', methods=PUT)
    @generic_response(PUT)
    def fn():
        return None, 'Invalid request body'

    response = client.put('/fake-put-error/')
    pytest.assume(response.status_code==400)
    pytest.assume(response.json['error']=='Invalid request body')