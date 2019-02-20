import re
from os import abort

from flask import request, jsonify

from app.api.responses import Responses
from app.api.routes.models.political import PoliticalParty as p
from urllib.parse import urlparse
from app.api.routes.models.office import GovernmentOffice as g

def check_password_hash(password_hash, password):
    print("kkkkkkkkk")
    return check_password_hash(password_hash, (password))

class Validations:



    @staticmethod
    def verify_political_details():
        """check that political party details are valid"""
        data = request.get_json()
        name = data['name'].strip()
        hqAddress = data['hqAddress'].strip()
        logoUrl = data['logoUrl'].strip()
        if len(name) == 0:
            return Responses.bad_request("Name cannot be empty"), 400
        if len(hqAddress) == 0:
            return Responses.bad_request("hqAddress name cannot be empty"), 400
        if len(logoUrl) == 0:
            return Responses.bad_request("LogoUrl cannot be empty"), 400

    @staticmethod
    def validate_characters():
        "this validates a party details"

        data = request.get_json()
        name = data['name'].strip()
        hqAddress = data['hqAddress'].strip()
        is_valid_name = r'[a-z]+'
        if len(name) < 6:
            return Responses.bad_request("Name should have more than 6 charcaters"), 400
        if len(hqAddress) < 6:
            return Responses.bad_request("hqAddress should have more than 6 charcaters"), 400
        party_exist = p.find_party_by_name(name)
        if party_exist:
            return Responses.bad_request({"Message": "Sorry, the party already exists"}), 400

    @staticmethod
    def validate_logo():
        """this validates logoUrl format"""
        data = request.get_json()
        url = urlparse(data['logoUrl'])
        if not url.scheme:
            return Responses.bad_request("incorrect format, url should start with the format http or https"), 403
        if not url.netloc:
            return Responses.bad_request("url should have a valid body format eg www.twitter.com"), 403
        if not url.path:
            return Responses.bad_request("url should have a path format of /pic.jpg"), 403

    @staticmethod
    def validate_strings(data):
        """ this ensures that all inputs are in the correct format"""
        if not isinstance(data['name'], str) or not isinstance(data['hqAddress'], str) or not isinstance(
                data['logoUrl'], str):
            return Responses.bad_request('Ensure that all inputs are strings'), 400

    @staticmethod
    def validate_json_inputs():
        """this check that json keys are not missing"""
        data = request.get_json()
        if not data:
            return Responses.bad_request("Empty inputs in Json"), 400
        if 'name' not in data:
            return Responses.bad_request("Name input is missing"), 400
        if 'hqAddress' not in data:
            return Responses.bad_request("hqAddress input is missing"), 400
        if 'logoUrl' not in data:
            return Responses.bad_request("logoUrl input is missing"), 400

    @staticmethod
    def validate_extra_fields(data):
        """this checks for extra keys in json format"""
        required_fields = ['name', 'hqAddress', 'logoUrl']
        if len(required_fields) < len(data.keys()):
            for key in data:
                if key not in required_fields:
                    return Responses.bad_request("{} is not a valid key".format(key)), 400

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
        office_exist = g.find_office_by_name(name)
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
        office_exist = g.find_office_by_name(name)
        if office_exist:
            return Responses.bad_request({"Message": "Sorry, the office already exists"}), 404

    @staticmethod
    def validate_admin(email):
        if email != "peris@gmail.com":
            abort(Responses.bad_request("You are not an admin"))
