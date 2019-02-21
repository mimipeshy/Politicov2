from flask import jsonify, request
from flask_jwt_extended import jwt_required

from app.api.blueprints import version2
from app.api.routes.models.candidate import Candidates as c
from app.api.routes.models.office import GovernmentOffice as ofisi
from app.api.validations.utils import Validations


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
# @jwt_required
def get_all_offices():
    """this returns all offices"""

    return ofisi.get_all_offices()


@version2.route("/office/<int:id>", methods=['GET'])
def get_one_office(id):
    """this gets one specific office"""
    return ofisi.get_one_office(id)


@version2.route("/office/register", methods=['POST'])
def register_candidate():
    """an admin can register a candidate to the office"""
    post_data = request.get_json()
    candidate = post_data['candidate']
    office = post_data['office']
    res = c.save_candidate(candidate, office)

    return res


@version2.route("/office/<int:office_id>/result", methods=["GET"])
# @jwt_required
def get_office_results(office_id):
    return ofisi.get_specific_results(office_id)
