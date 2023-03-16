import pytest

from app.controllers import ReportController


def test_get_report():
    report, error = ReportController.get_report()
    pytest.assume(report['best_customers'])
    pytest.assume(report['most_requested_ingredient'])
    pytest.assume(report['orders_by_month'])
    pytest.assume(error is None)


def test_get_orders_by_month():
    orders_by_month, error = ReportController.get_orders_by_month()
    pytest.assume(orders_by_month)
    pytest.assume(error is None)

def test_get_most_requested_ingredient():
    most_requested_ingredient, error = ReportController.get_most_requested_ingredient()
    pytest.assume(most_requested_ingredient['most_requested_ingredient_sum'])
    pytest.assume(most_requested_ingredient['most_requested_ingredient_count'])
    pytest.assume(error is None)


def test_get_best_customers():
    best_customers, error = ReportController.get_best_customers()
    pytest.assume(best_customers)
    pytest.assume(error is None)