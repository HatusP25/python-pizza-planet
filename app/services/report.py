from flask import Blueprint, jsonify

from app.controllers.report import ReportController

report = Blueprint('report', __name__)


@report.route('/', methods=['GET'])
def get_report():
    report_data, error = ReportController.get_report()
    response = report_data if not error else {'error': error}
    status_code = 200 if report_data else 404 if not error else 400
    return jsonify(response), status_code
