import pytest

from app.test.utils.functions import are_values_close

def test_get_report_service(create_report,report_uri, client):
    response = client.get(report_uri)
    pytest.assume(response.status.startswith('200'))
    expected_ingredient_report = create_report['ingredient_report']
    returned_ingredient_report = response.json['ingredient_report']
    print(expected_ingredient_report)
    print(returned_ingredient_report)
    for i in range(len(returned_ingredient_report)):
        pytest.assume(expected_ingredient_report[i]['ingredient_count'] == returned_ingredient_report[i]['ingredient_count'])
        
