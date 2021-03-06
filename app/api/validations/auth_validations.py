import re
from urllib.parse import urlparse

from flask import request
from werkzeug.security import generate_password_hash, check_password_hash

from app.api.responses import Responses


class AuthValidations:
    @staticmethod
    def hash_password(password):
        """
            Hashes the password using pbkdf2_sha512
        """
        hashed_password = generate_password_hash(password)
        return hashed_password

    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)

    @staticmethod
    def validate_extra_fields(data, required_fields):
        """this ensures no extra fields in json"""
        if len(required_fields) < len(data.keys()):
            for key in data:
                if key not in required_fields:
                    return Responses.bad_request({"Message": "{} is not a valid key".format(key)}), 400

    @staticmethod
    def check_for_blank_spaces(data, required_fields):
        """this checks and ensures no field has been left blank"""
        for key, value in data.items():
            if key in required_fields and not value.strip():
                return Responses.bad_request(
                    {"Message": '{} is a required field and cannot be left blank'.format(key)}), 400

    @staticmethod
    def check_email_is_valid(email):
        """this checks that the email is of the correct format"""
        email_address_matcher = re.compile('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        return True if email_address_matcher.match(email) else False

    @staticmethod
    def validate_len_characters(data,required_keys):
        "this validates a party details"
        for key, value in data.items():
            if len(required_keys) < 6:
                return Responses.bad_request({"Message": "{} should have more than 6 characters".format(key)}), 400

    @staticmethod
    def validate_strings(data):
        """ this ensures that all inputs are in the correct format"""
        if not isinstance(data['name'], str) or not isinstance(data['hqAddress'], str) or not isinstance(
                data['logoUrl'], str):
            return Responses.bad_request('Ensure that all inputs are strings'), 400

    @staticmethod
    def validate_logo():
        """this validates logoUrl format"""
        data = request.get_json()
        url = urlparse(data['logoUrl'])
        if not url.scheme:
            return Responses.bad_request("incorrect format, url should start with the format http or https"), 400
        if not url.netloc:
            return Responses.bad_request("url should have a valid body format eg www.twitter.com"), 400
        if not url.path:
            return Responses.bad_request("url should have a path format of /pic.jpg"), 400



