import pytest

def test_get_report_service(create_report):
    report = create_report.json
    pytest.assume(create_report.status.startswith('200'))
    pytest.assume(report['best_customers'])
    pytest.assume(report['most_requested_ingredient'])
    pytest.assume(report['orders_by_month'])
