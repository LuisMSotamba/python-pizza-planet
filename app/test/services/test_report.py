import pytest

def test_get_report_service(create_report,report_uri, client):
    response = client.get(report_uri)
    pytest.assume(response.status.startswith('200'))
    expected_ingredient_report = create_report['ingredient_report']
    returned_ingredient_report = response.json['ingredient_report']
    for i in range(len(returned_ingredient_report)):
        # the others fields don't be taken into account because they can vary when the 
        # ingredient_count field is the same for 2 or more ingredients
        pytest.assume(expected_ingredient_report[i]['ingredient_count'] == returned_ingredient_report[i]['ingredient_count'])
    
    expected_order_report = create_report['order_report']
    returned_order_report = response.json['order_report']
    for i in range(len(returned_order_report)):
        pytest.assume(expected_order_report[i]['month'] == returned_order_report[i]['month'])
        pytest.assume(expected_order_report[i]['revenue'] == returned_order_report[i]['revenue'])
    
    expected_customer_report = create_report['customer_report']
    returned_customer_report = response.json['customer_report']
    for i in range(len(returned_customer_report)):
        # customer name and customer dni don't be taken into account because they can vary 
        # when the total_money is the same for 2 or more customers
        pytest.assume(expected_customer_report[i]['total_money'] == returned_customer_report[i]['total_money'])
