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
        is_admin = data['is_admin']
        email = data['email']

    except:
        return Responses.bad_request('Check your json keys. '
                                     'first_name, last_name, other_name,'
                                     'phone_number, email, password,is_admin, passportUrl', )
    validate.validate_extra()
    validate.check_for_strings(data, ['first_name', 'last_name', 'other_name', 'email', 'is_admin', 'password'])
    validate.check_for_blank_spaces(data,
                                    ['first_name', 'last_name', 'other_name', 'email', 'phone', 'is_admin', 'password'])
    validate.check_email_is_valid(email)
    validate.check_valid_phone_number(phone_number)
    user_exist = u.get_one_by_email(email)
    if user_exist:
        return Responses.bad_request({"Message": "User already exists, please login"}), 404
    user = u(first_name, last_name, other_name, email, phone_number, password, passportUrl, is_admin)
    user_id = user.save(is_admin)
    token = create_access_token(identity=email)
    return make_response(jsonify({"Data": "User {} registered".format(email),
                                  "token": token}),201)


@version2.route("/auth/login", methods=['POST'])
def login_user():
    """this logs in a registered user"""
    try:
        if request.content_type == 'application/json':
            data = request.get_json(force=True)
            password = data['password']
            email = data['email']
            if not email:
                return Responses.bad_request('Your email is missing!')
            if not validate.check_email_is_valid(email):
                return Responses.bad_request('Your email is invalid! Kindly recheck your email.')
            user = u.get_one_by_email(email)
            # user_id = u.get_one_by_id(user)
            if not user:
                return Responses.bad_request('User does not exist. Kindly register!')
            else:
                if email and password:
                    password_hash = u.get_password(email)[0]
                    if check_password(password_hash,password):
                        token = create_access_token(identity=email)
                        if token:
                            return make_response(jsonify({"Success": 'You have logged in successfully!',
                                                          "token": token}))
                    else:
                        return Responses.bad_request('Wrong Password!')
                else:
                    if not password:
                        return Responses.bad_request('Your password is missing!')
        return Responses.bad_request('Content-Type must be JSON.')
    except errors.BadRequest as e:
        return e.message
    except errors.NotFound as e:
        return e.message
    except errors.Unauthorized as e:
        return e.message
    except Exception as error:

        return make_response(jsonify({"error": "Please provide for all the fields. Missing field: " + str(error)}), 400)
