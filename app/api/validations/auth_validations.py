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
            return Responses.bad_request("incorrect format, url should start with the format http or https"), 403
        if not url.netloc:
            return Responses.bad_request("url should have a valid body format eg www.twitter.com"), 403
        if not url.path:
            return Responses.bad_request("url should have a path format of /pic.jpg"), 403

    @staticmethod
    def is_valid_string(string_provided):
        """
        This function returns True
        if the item provided is a string
        and is not empty
        """
        if string_provided:
            return isinstance(string_provided, str)
        else:
            return False

    @staticmethod
    def check_int(val):
        """this checks if a number is an integer"""
        return isinstance(val, int)

    @staticmethod
    def check_for_strings(data, checklist):

        """this ensures that an input is not a string"""
        return AuthValidations.type_checks(AuthValidations.is_valid_string, "field cannot be a non string.", data, checklist)

    @staticmethod
    def type_checks(pred, errormessage, data, checklist):
        """
            this function checks that values provided in the data args
            conform or pass the pred function test.
            if they dont pass, an error is thrown
        """
        for key, value in data.items():
            if key in checklist and not pred(value):
                return Responses.bad_request('{} {}'.format(key, errormessage))

    @staticmethod
    def check_valid_phone_number(phone_number):
        """This checks if a number phone number is valid"""
        if not re.match('^[0-9]*$', phone_number):
            return Responses.bad_request({"Phone number should only contain numbers"}), 400
        return True


