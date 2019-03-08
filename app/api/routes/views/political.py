from flask import request, jsonify, make_response

from app.api.blueprints import version2
from app.api.responses import Responses
from app.api.routes.models.political import PoliticalParty as p
from app.api.validations.auth_validations import AuthValidations as v

parties = []
political_obj = p()


@version2.route("/party", methods=['POST'])
# @jwt_required
def create_political_party():
    """this creates a new political party"""

    data = request.get_json(force=True)
    required_fields = ["name", "hqAddress", "logoUrl"]
    empty_fields = v.check_for_blank_spaces(data, required_fields=required_fields)
    if empty_fields:
        return v.check_for_blank_spaces(data, required_fields=required_fields)  # checks for empty fields
    extra_fields = v.validate_extra_fields(data, required_fields=required_fields)
    if extra_fields:
        return v.validate_extra_fields(data, required_fields=required_fields)  # checks for extra
        # fields
    valid_string = v.validate_strings(data)
    if valid_string:
        return v.validate_strings(data)
    len = v.validate_len_characters(data, required_keys=required_fields)
    if len:
        return v.validate_len_characters(data, required_keys=required_fields)  # checks for length of fields
    chk_logo= v.validate_logo()
    if chk_logo:
        return chk_logo
    name = data['name']
    hqAddress = data['hqAddress']
    logoUrl = data['logoUrl']

    new = p(name, hqAddress, logoUrl)
    party_exist = political_obj.find_party_by_name(name)
    if party_exist:
        return Responses.bad_request({"Message": "Sorry, the party already exists"}), 400
    party = new.save()
    return make_response(jsonify({
        "id": party[0],
        "Status": "OK",
        "Message": "Party created successfully",
        "Party Details": party[1],
        "hqAddress": party[2],
        "logoUrl": party[3]
    }), 201)

@version2.route("/party", methods=['GET'])
def get_all_parties():
    return political_obj.get_all_parties()


@version2.route("/party/<int:party_id>", methods=['GET'])
def get_one_party(party_id):
    return political_obj.get_one_party(party_id)


@version2.route("/party/<int:party_id>/name", methods=['PATCH'])
def get_update_party(party_id):
    return political_obj.update_party(party_id)


@version2.route("/party/<int:party_id>", methods=['DELETE'])
def delete_specific_party(party_id):
    data = political_obj.find_party_by_id(party_id)
    if data:
        political_obj.delete_party(party_id)
        return make_response(jsonify({
            "status": "OK",
            "Message": "Party deleted"
        }), 200)
    return make_response(jsonify({
        "status": "OK",
        "Party": "Political party not found"
    }), 404)
