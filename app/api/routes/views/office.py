from flask import jsonify, make_response, request
from app.api.responses import Responses

from app.api.blueprints import version2
from app.api.routes.models.office import GovernmentOffice as ofisi
from app.api.utils import Validations


@version2.route("/office", methods=['POST'])
def create_an_office():
    """this creates a new office"""
    data = request.get_json()
    valid = Validations.create_office()
    if valid:
        return Validations.create_office()
    name = data['name']
    type = data['type']
    final = ofisi(name, type)
    response = final.add_political_office(name, type)
    result = [{"id": response[0], "name": response[1], "type": response[2]}]
    return jsonify({"msg": result}), 201


@version2.route("/office", methods=['GET'])
def get_all_offices():
    """this returns all offices"""

    return ofisi.get_all_offices()


@version2.route("/office/<int:id>", methods=['GET'])
def get_one_office(id):
    """this gets one specific office"""
    return ofisi.get_one_office(id)
