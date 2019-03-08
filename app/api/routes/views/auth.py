from flask import request, make_response, jsonify
from flask_jwt_extended import create_access_token

import app.api.responses as errors
from app.api.blueprints import version2
from app.api.responses import Responses
from app.api.routes.models.user import UserModel as u
from app.api.validations.auth_validations import AuthValidations as v

user_object = u()


@version2.route("/auth/signup", methods=['POST'])
def register_new_user():
    """this class registers a new user"""
    try:
        data = request.get_json()
        first_name = data['first_name']
        last_name = data['last_name']
        other_name = data['other_name']
        phone_number = data['phone_number']
        password = data['password']
        passportUrl = data['passportUrl']
        email = data['email']
    except:
        return Responses.bad_request('Check your json keys. '
                                     'first_name, last_name, other_name,'
                                     'phone_number, email, password, passportUrl', )
    required_fields = ['first_name', 'last_name', 'other_name', 'phone_number', 'email',
                       'password', 'passportUrl',
                       'is_admin']
    error = v.validate_extra_fields(data,
                                    required_fields=required_fields)
    if error:
        return v.validate_extra_fields(data, required_fields=required_fields)
    empty = v.check_for_blank_spaces(data,
                                     required_fields=required_fields)
    if empty:
        return v.check_for_blank_spaces(data, required_fields=required_fields)
    valid_email = v.check_email_is_valid(email)
    if not valid_email:
        return Responses.bad_request("Invalid email url format"), 400
    user_exist = user_object.get_one_by_email(email)
    if user_exist:
        return Responses.bad_request({"Message": "User already exists, please login"}), 400
    is_admin = False
    user_ob = u(first_name, last_name, other_name, email, phone_number, password, passportUrl, is_admin)
    user_ob.save()
    res = Responses.created_response({"Message": "User created successfully",
                                      "First_name": first_name,
                                      "Last_name": last_name,
                                      "Phone Number": phone_number,
                                      "Email Address": email,
                                      "is_admin": is_admin
                                      }), 201
    return res


@version2.route("/auth/login", methods=['POST'])
def login_user():
    """this logs in a registered user"""
    try:
        if request.content_type == 'application/json':
            data = request.get_json(force=True)
            password = data['password']
            email = data['email']
            if not email:
                return Responses.not_found({"Message": 'Your email is missing!'}), 404
            if not password:
                return Responses.bad_request({"Message": 'Your password is missing!'}), 404
            if not v.check_email_is_valid(email):
                return Responses.not_found({"Message": 'Your email is invalid! Kindly recheck your email.'}), 404
            user = user_object.get_one_by_email(email)
            if not user:
                return Responses.not_found({"Message": 'User does not exist. Kindly register!'}), 404
            else:
                if email and password:
                    password_hash = user_object.get_password(email)[0]
                    if v.check_password(password_hash, password):
                        token = create_access_token(identity=email)
                        if token:
                            return make_response(jsonify({"Success": 'You have logged in successfully!',
                                                          "token": token}), 200)
                    else:
                        return Responses.bad_request({"Message": 'Wrong Password!'}), 404
        return Responses.bad_request({"Message": 'Content-Type must be JSON.'}), 400
    except:
        return Responses.bad_request(
            {"Message": "Please provide for all the fields. Missing field:  email, password"}), 400
