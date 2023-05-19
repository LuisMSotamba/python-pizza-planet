from ..repositories.managers import ReportManager
from .base import BaseController


class ReportController(BaseController):
    manager = ReportManager

    @classmethod
    def get_statistics(cls):
        return cls.manager.get_statistics(), None