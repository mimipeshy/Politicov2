import re
from os import abort

from flask import request
from werkzeug.security import generate_password_hash, check_password_hash

from app.api.responses import Responses


def check_int(val):
    """this checks if a number is an integer"""
    return isinstance(val, int)


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


def check_valid_phone_number(phone_number):
    """This checks if a number phone number is valid"""
    if not re.match('^[0-9]*$', phone_number):
        return Responses.bad_request({"Phone number should only contain numbers"}), 400
    return True


def check_for_blank_spaces(data, required_fields):
    """this checks and ensures no field has been left blank"""
    for key, value in data.items():
        if key in required_fields and not value.strip():
            return Responses.bad_request('{} is a required field and cannot be left blank'.format(key))
    return True


def check_email_is_valid(email):
    """this checks that the email is of the correct format"""
    email_regex = re.compile('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$')
    if not re.match(email_regex, email):
        return Responses.not_found("invalid email")


def check_for_strings(data, checklist):
    """this ensures that an input is not a string"""
    return type_checks(is_valid_string, "field cannot be a non string.", data, checklist)


def type_checks(pred, errormessage, data, checklist):
    """
        this function checks that values provided in the data args
        conform or pass the pred function test.
        if they dont pass, an error is thrown
    """
    for key, value in data.items():
        if key in checklist and not pred(value):
            abort(Responses.bad_request('{} {}'.format(key, errormessage)))
    return True


def validate_extra():
    """this ensures no extra fields in json"""
    data = request.get_json()
    required_fields = ['first_name', 'last_name', 'other_name', 'email', 'password', 'passportUrl', 'is_admin']
    if len(required_fields) < len(data.keys()):
        for key in data:
            if key not in required_fields:
                return Responses.bad_request("{} is not a valid key".format(key)), 400


def hash_password(password):
    """
        Hashes the password using pbkdf2_sha512
        :param password: The sha512 password from the login/register form
        :return: A sha512 -> pbkdf2_sha512 encrypted password
        """
    return generate_password_hash(password)


def check_hashed_password(password, hashed_password):
    """
        Checked that the password the user sent matches that of the database.
        The database password is encrypted more than the user's password at the stage
        :param password: sha512-ashed password
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return: True if passwords match, False otherwise
        """
    return check_password_hash(hashed_password, password)
