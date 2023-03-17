from flask import jsonify, request


class BaseService:

    def __init__(self, EntityController):
        self.controller = EntityController

    def create(self):
        entity, error = self.controller.create(request.json)
        response, status_code = self.__obtain_response(entity, error)
        return jsonify(response), status_code

    def update(self):
        entity, error = self.controller.update(request.json)
        response, status_code = self.__obtain_response(entity, error)
        return jsonify(response), status_code

    def get_by_id(self, _id: int):
        entity, error = self.controller.get_by_id(_id)
        response, status_code = self.__obtain_response(entity, error)
        return jsonify(response), status_code

    def get_all(self):
        entities, error = self.controller.get_all()
        response, status_code = self.__obtain_response(entities, error)
        return jsonify(response), status_code

    def __obtain_response(self, entity, error):
        response = entity if not error else {'error': error}
        status_code = 200 if not error else 400 if entity else 404
        return response, status_code
