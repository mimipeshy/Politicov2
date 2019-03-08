import re
from os import abort

from flask import request, jsonify

from app.api.responses import Responses
from app.api.routes.models.political import PoliticalParty as p
from urllib.parse import urlparse
from app.api.routes.models.office import GovernmentOffice as g

political_obj = p()
office_obj = g()


class Validations:

    @staticmethod
    def create_office():
        data = request.get_json()
        required_fields = ['name', 'type']
        if not data:
            return Responses.bad_request("Empty inputs in Json"), 400
        if 'name' not in data:
            return Responses.bad_request("name input is missing"), 400
        if 'type' not in data:
            return Responses.bad_request("type input is missing"), 400
        if len(required_fields) < len(data.keys()):
            for key in data:
                if key not in required_fields:
                    return Responses.bad_request("{} is not a valid key".format(key)), 400
        if not isinstance(data['name'], str) or not isinstance(data['type'], str):
            return Responses.bad_request('Ensure that all inputs are strings'), 400
        name = data['name'].strip()
        type = data['type'].strip()
        if len(name) == 0:
            return Responses.bad_request("Office Name cannot be empty"), 400
        if len(type) == 0:
            return Responses.bad_request("Type cannot be empty"), 400
        if len(name) < 6:
            return Responses.bad_request("Office Name should have more than 6 characters"), 400
        office_exist = office_obj.find_office_by_name(name)
        if office_exist:
            return Responses.bad_request({"Message": "Sorry, the office already exists"}), 404

    @staticmethod
    def validate_update_all():
        data = request.get_json()

        required_fields = ['name']
        if not data:
            return Responses.bad_request("Empty inputs in Json"), 400
        if 'name' not in data:
            return Responses.bad_request("name input is missing"), 400
        if len(required_fields) < len(data.keys()):
            for key in data:
                if key not in required_fields:
                    return Responses.bad_request("{} is not a valid key".format(key)), 400
        if not isinstance(data['name'], str):
            return Responses.bad_request('Ensure that all inputs are strings'), 400
        name = data['name'].strip()
        if len(name) == 0:
            return Responses.bad_request("Party Name cannot be empty"), 400
        if len(name) < 6:
            return Responses.bad_request("Name should have more than 6 characters"), 400
        if not isinstance(data['name'], str):
            return Responses.bad_request('Ensure that all name input is a string'), 400
        office_exist = office_obj.find_office_by_name(name)
        if office_exist:
            return Responses.bad_request({"Message": "Sorry, the office already exists"}), 404

    @staticmethod
    def validate_admin(email):
        if email != "peris@gmail.com":
            abort(Responses.bad_request("You are not an admin"))