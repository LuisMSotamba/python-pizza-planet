import pytest

from app.test.utils.functions import get_random_string, get_random_price


def test_create_size_service(size, client):
    response = client.post('/size/',json=size)
    pytest.assume(response.status.startswith('201'))
    pytest.assume(response.json['_id'])
    pytest.assume(response.json['name'])
    pytest.assume(response.json['price'])


def test_update_size_service(create_size, client, size_uri):
    current_size = create_size
    update_data = {**current_size, 'name': get_random_string(), 'price': get_random_price(1, 5)}
    response = client.put(size_uri, json=update_data)
    pytest.assume(response.status.startswith('200'))
    updated_size = response.json
    for param, value in update_data.items():
        pytest.assume(updated_size[param] == value)


def test_get_size_by_id_service(client, create_size, size_uri):
    current_size = create_size
    response = client.get(f'{size_uri}id/{current_size["_id"]}')
    pytest.assume(response.status.startswith('200'))
    returned_size = response.json
    for param, value in current_size.items():
        pytest.assume(returned_size[param] == value)

def test_get_non_existent_size_by_id_service(client, size_uri):
    response = client.get(f'{size_uri}id/1')
    pytest.assume(response.status.startswith('404'))

def test_get_sizes_service(client, create_sizes, size_uri):
    response = client.get(size_uri)
    pytest.assume(response.status.startswith('200'))
    returned_sizes = {size['_id']: size for size in response.json}
    for size in create_sizes:
        pytest.assume(size['_id'] in returned_sizes)

def test_get_non_existent_sizes_service(client, size_uri):
    response = client.get(size_uri)
    pytest.assume(response.status.startswith('404'))
