from flask import Blueprint

from app.common.http_methods import GET, POST, PUT
from .BaseService import BaseService


class BaseBlueprint(Blueprint):
    def __init__(self, name, import_name, controller_class):
        super().__init__(name, import_name)
        self.service = BaseService(controller_class)

        self.add_url_rule('/', methods=POST, view_func=self.create)
        self.add_url_rule('/', methods=PUT, view_func=self.update)
        self.add_url_rule('/id/<int:_id>', methods=GET, view_func=self.get_by_id)
        self.add_url_rule('/', methods=GET, view_func=self.get_all)

    def create(self):
        return self.service.create()

    def update(self):
        return self.service.update()

    def get_by_id(self, _id: int):
        return self.service.get_by_id(_id)

    def get_all(self):
        return self.service.get_all()

