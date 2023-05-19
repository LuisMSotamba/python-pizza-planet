import pytest

@pytest.fixture
def report_uri():
    return '/report/'


@pytest.fixture
def create_ingredients_report(create_orders):
    ingredient_ids = {}
    for order in create_orders:
        for detail in order.json['detail']:
            if detail['ingredient']['_id'] in ingredient_ids:
                ingredient_ids[detail['ingredient']['_id']]['ingredient_count'] += 1.0
            else:
                ingredient_ids[detail['ingredient']['_id']] = {
                    'ingredient': detail['ingredient'],
                    'ingredient_count': 1.0
                }
    ingredient_report = [ ingredient_range for ingredient_range in ingredient_ids.values() ]
    return sorted(ingredient_report, key=lambda x: x['ingredient_count'], reverse=True)

@pytest.fixture
def create_report(create_ingredients_report):
    report = {}
    report['ingredient_report'] = create_ingredients_report
    return report
