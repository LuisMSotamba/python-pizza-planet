from datetime import datetime

import pytest
import calendar

@pytest.fixture
def report_uri():
    return '/report/'


def create_ingredients_report(orders):
    ingredient_ids = {}
    for order in orders:
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

def create_order_report(orders):
    order_report = {}    
    for order in orders:
        _order = order.json
        date_object = datetime.strptime(_order['date'], '%Y-%m-%dT%H:%M:%S.%f')
        month = calendar.month_name[date_object.month]
        if month in order_report:
            order_report[month]['revenue'] += _order['total_price']
        else:
            order_report[month] = {
                'month': month,
                'revenue': _order['total_price']
            }
    order_report = [order_range for order_range in order_report.values()]
    return sorted(order_report, key=lambda x: x['revenue'], reverse=True)


def create_customer_report(orders):
    customer_report = {}
    for order in orders:
        _order = order.json
        if _order['client_name'] in customer_report:
            customer_report[_order['client_name']]['total_money'] += _order['total_price']
        else:
            customer_report[_order['client_name']] = {
                'customer_dni': _order['client_name'],
                'customer_name': _order['client_name'],
                'total_money': _order['total_price']
            }
    customer_report = [customer_range for customer_range in customer_report.values()]
    return sorted(customer_report, key=lambda x: x['total_money'], reverse=True)


@pytest.fixture
def create_report(create_orders):
    report = {}
    report['ingredient_report'] = create_ingredients_report(create_orders)
    report['order_report'] = create_order_report(create_orders)
    report['customer_report'] = create_customer_report(create_orders)
    return report
