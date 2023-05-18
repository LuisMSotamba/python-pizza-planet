import pytest

from app.test.utils.functions import get_random_string, get_random_price


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
