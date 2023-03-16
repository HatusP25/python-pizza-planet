from app.controllers.base import BaseController
from app.repositories.managers import ReportManager


class ReportController(BaseController):
    manager = ReportManager

    @classmethod
    def get_orders_by_month(cls):
        return cls.manager.get_orders_by_month()

    @classmethod
    def get_most_requested_ingredient(cls):
        return cls.manager.get_most_requested_ingredient()

    @classmethod
    def get_best_customers(cls):
        return cls.manager.get_best_customers()

    @classmethod
    def get_report(cls):
        report = {
            'orders_by_month': cls.get_orders_by_month(),
            'most_requested_ingredient': cls.get_most_requested_ingredient(),
            'best_customers': cls.get_best_customers()
        }
        return report, None
