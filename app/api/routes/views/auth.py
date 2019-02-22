import re

from flask import make_response
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from app.api.responses import Responses
from app.api.blueprints import version2
from app.api.routes.models.user import UserModel as u
import app.api.validations.validation as validate
from app.api.validations.validation import check_password
import app.api.responses as errors
from app.api.validations.utils import Validations

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
                                     'phone_number, email, password, passportUrl'),400
    validate.validate_extra()
    validate.check_for_strings(data, ['first_name', 'last_name', 'other_name', 'email',  'password'])
    Validations.verify_user_signup()
    email_regex = re.compile('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$')
    if not re.match(email_regex, email):
        return Responses.not_found("invalid email")
    if not re.search("((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[$#@]).{6,12})", password):
        return Responses.not_found("Password should contain atleast a letter, symbol,uppercase and lowercase characters")


    user_exist = user_object.get_one_by_email(email)
    if user_exist:
        return Responses.bad_request({"Message": "User already exists, please login"})
    is_admin = False
    user_ob = u(first_name, last_name, other_name, email, phone_number, password, passportUrl, is_admin)
    user_ob.save()
    token = create_access_token(identity=email, )
    return make_response(jsonify({"Data": "User {} registered".format(email),
                                  "is_admin":is_admin,
                                  "token": token}), 201)


@version2.route("/auth/login", methods=['POST'])
def login_user():
    """this logs in a registered user"""
    try:
        if request.content_type == 'application/json':
            data = request.get_json(force=True)
            password = data['password']
            email = data['email']
            if not email:

                return Responses.not_found('Your email is missing!'),400
            if not validate.check_email_is_valid(email):

                return Responses.not_found('Your email is invalid! Kindly recheck your email.'),400
            user = user_object.get_one_by_email(email)
            if not user:
                return Responses.not_found('User does not exist. Kindly register!'),404
            else:
                if email and password:
                    password_hash = user_object.get_password(email)[0]
                    if check_password(password_hash, password):
                        token = create_access_token(identity=email)
                        if token:
                            return make_response(jsonify({"Success": 'You have logged in successfully!',
                                                          "token": token}), 200)
                    else:
                        return Responses.bad_request('Wrong Password!')
                else:
                    if not password:
                        return Responses.bad_request('Your password is missing!'),400
        return Responses.bad_request('Content-Type must be JSON.'),400
    except errors.BadRequest as e:
        return e.message
    except errors.NotFound as e:
        return e.message
    except errors.Unauthorized as e:
        return e.message
    except Exception as error:
        return make_response(jsonify({"error": "Please provide for all the fields. Missing field: " + str(error)}), 400)
