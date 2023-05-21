from app.common.http_methods import GET
from flask import Blueprint, jsonify, request

from ..controllers import ReportController
from app.common.decorators import generic_response

report = Blueprint('report', __name__)


@report.route('/', methods=GET)
@generic_response(GET)
def get_report():
    report, error = ReportController.get_statistics()
    return report, error