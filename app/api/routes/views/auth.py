from flask import make_response
from flask import request, jsonify
from app.api.responses import Responses
from app.api.blueprints import version2
from app.api.routes.models.user import UserModel as u
import app.api.validation as validate
import app.api.validations.common as tokens

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
    user = u(first_name, last_name, other_name, email, password, phone_number, passportUrl, is_admin)
    user.save(first_name, last_name, other_name, email, password, phone_number, passportUrl, is_admin)
    user_id = u.get_one_by_email(email)

    access_token = tokens.generate_token(user_id)
    return make_response(jsonify({"Data": "User {} registered".format(email),
                                  "token": access_token.decode()}))



