import pytest

def test_create_beverage_service(create_beverage):
    beverage = create_beverage.json
    pytest.assume(create_beverage.status.startswith('201'))
    pytest.assume(beverage['_id'])
    pytest.assume(beverage['name'])
    pytest.assume(beverage['price'])

def test_get_beverages_service(client, create_beverages, beverage_uri):
    response = client.get(beverage_uri)
    pytest.assume(response.status.startswith('200'))
    returned_beverages = {beverage['_id']: beverage for beverage in response.json}
    for beverage in create_beverages:
        pytest.assume(beverage['_id'] in returned_beverages)
