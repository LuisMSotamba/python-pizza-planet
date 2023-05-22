import pytest

def test_create_order_service(order, client, order_uri):
    response = client.post(order_uri, json=order)
    order_response = response.json
    pytest.assume(response.status.startswith('201'))
    pytest.assume(order_response['_id'])
    pytest.assume(order_response['client_name'])
    pytest.assume(order_response['client_dni'])
    pytest.assume(order_response['client_address'])
    pytest.assume(order_response['client_phone'])
    pytest.assume(order_response['date'])
    pytest.assume(order_response['total_price'])
    pytest.assume(order_response['size'])
    pytest.assume(order_response['detail'])
    pytest.assume(order_response['beverage_detail'])

def test_get_order_by_id_service(create_order, order_uri, client):
    current_order = create_order.json
    response = client.get(f'{order_uri}id/{current_order["_id"]}')
    pytest.assume(response.status.startswith('200'))
    returned_ingredient = response.json
    for param, value in current_order.items():
        pytest.assume(returned_ingredient[param] == value)

def test_get_non_existent_order_by_id_service(order_uri, client):
    response = client.get(f'{order_uri}id/10')
    pytest.assume(response.status.startswith('404'))

def test_get_orders_service(client, create_orders, order_uri):
    response = client.get(order_uri)
    pytest.assume(response.status.startswith('200'))
    returned_ingredients = {ingredient['_id']: ingredient for ingredient in response.json}
    for ingredient in create_orders:
        pytest.assume(ingredient['_id'] in returned_ingredients)

def test_get_non_existent_orders_service(client, order_uri):
    response = client.get(order_uri)
    pytest.assume(response.status.startswith('404'))