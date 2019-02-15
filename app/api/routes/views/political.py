from flask import request, jsonify, make_response

from app.api.blueprints import version2
from app.api.routes.models.political import PoliticalParty as p
from app.api.utils import Validations

parties = []


@version2.route("/party", methods=['POST'])
def create_political_party():
    """this creates a new political party"""

    data = request.get_json(force=True)
    empty = Validations.validate_json_inputs()
    if empty:
        return Validations.validate_json_inputs()
    error = Validations.validate_extra_fields(data)
    if error:
        return Validations.validate_extra_fields(data)
    validate = Validations.validate_strings(data)
    if validate:
        return Validations.validate_strings(data)
    # create a party
    if Validations.verify_political_details():
        return Validations.verify_political_details()
    if Validations.validate_characters():
        return Validations.validate_characters()
    if Validations.validate_logo():
        return Validations.validate_logo()
    name = data['name']
    hqAddress = data['hqAddress']
    logoUrl = data['logoUrl']

    new = p(name, hqAddress, logoUrl)
    party = new.save(name, hqAddress, logoUrl)
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
    return p.get_all_parties()


@version2.route("/party/<int:party_id>", methods=['GET'])
def get_one_party(party_id):
    return p.get_one_party(party_id)


@version2.route("/party/<int:party_id>/name", methods=['PATCH'])
def get_update_party(party_id):
    return p.update_party(party_id)
