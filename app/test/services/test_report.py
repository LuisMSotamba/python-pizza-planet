import pytest

def test_get_report_service(create_report,report_uri, client):
    response = client.get(report_uri)
    pytest.assume(response.status.startswith('200'))
    expected_ingredient_report = create_report['ingredient_report']
    returned_ingredient_report = response.json['ingredient_report']
    for i in range(len(returned_ingredient_report)):
        pytest.assume(expected_ingredient_report[i]['ingredient_count'] == returned_ingredient_report[i]['ingredient_count'])
    expected_order_report = create_report['order_report']
    returned_order_report = response.json['order_report']
    for i in range(len(returned_order_report)):
        pytest.assume(expected_order_report[i]['month'] == returned_order_report[i]['month'])
        pytest.assume(expected_order_report[i]['revenue'] == returned_order_report[i]['revenue'])
    
