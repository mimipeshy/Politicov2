from flask import jsonify, request
from flask_jwt_extended import jwt_required

from app.api.blueprints import version2
from app.api.responses import Responses
from app.api.routes.models.candidate import Candidates as c
from app.api.routes.models.office import GovernmentOffice as ofisi
from app.api.validations.auth_validations import AuthValidations as v

candidate_obj = c()
office_obj = ofisi()


@version2.route("/office", methods=['POST'])
@jwt_required
def create_an_office():
    """this creates a new office"""
    try:
        data = request.get_json()
        required_fields = ["name", "type"]
        empty_fields = v.check_for_blank_spaces(data, required_fields=required_fields)
        if empty_fields:
            return v.check_for_blank_spaces(data, required_fields=required_fields)  # checks for empty fields
        extra_fields = v.validate_extra_fields(data, required_fields=required_fields)
        if extra_fields:
            return v.validate_extra_fields(data, required_fields=required_fields)  # checks for extra
            # fields
        name = data['name']
        type = data['type']
        office_exist = office_obj.find_office_by_name(name)
        if office_exist:
            return Responses.bad_request({"Message": "Sorry, the office already exists"}), 404
        final = ofisi(name, type)
        response = final.add_political_office()
        result = [{"id": response[0], "name": response[1], "type": response[2]}]
        return jsonify({"msg": result}), 201
    except:
        return Responses.bad_request({"Message": 'Content-Type must be JSON.'}), 400


@version2.route("/office", methods=['GET'])
@jwt_required
def get_all_offices():
    """this returns all offices"""

    return office_obj.get_all_offices()


@version2.route("/office/<int:id>", methods=['GET'])
@jwt_required
def get_one_office(id):
    """this gets one specific office"""
    return office_obj.get_one_office(id)


@version2.route("/office/register", methods=['POST'])
@jwt_required
def register_candidate():
    """an admin can register a candidate to the office"""
    post_data = request.get_json()
    if not post_data:
        return Responses.bad_request('Invalid your json keys. Use these keys '
                                     'office, candidate ')
    candidate = post_data['candidate']
    office = post_data['office']
    candidate_object = c(candidate, office)
    res = candidate_object.save_candidate()
    return res


@version2.route("/office/<int:office_id>/result", methods=["GET"])
@jwt_required
def get_office_results(office_id):
    return office_obj.get_specific_results(office_id)
