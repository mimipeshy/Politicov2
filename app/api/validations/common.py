from datetime import datetime, timedelta

import jwt
from flask import current_app
from app.api.routes.models.user import UserModel as User
from app.api.responses import Responses


def generate_token(user_id):
    """
    Generates authentication token.

    """
    try:

        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=600),
            'iat': datetime.utcnow(),
            'user_id': user_id,
            # 'is_admin':role [0]
        }
        # create byte string token using payload and secret key
        jwt_string = jwt.encode(
            payload,
            current_app.config['SECRET'],
            algorithm='HS256')
        return jwt_string
    except Exception as e:
        return str(e)


def decode_token(access_token):
    """
    Decode the access token from the authorization.

    """
    try:
        payload = jwt.decode(access_token, current_app.config['SECRET'])
        return payload
    except jwt.ExpiredSignatureError:
        raise Responses.bad_request("Signature Expired. Please login!")
    except jwt.InvalidTokenError:
        raise Responses.bad_request("Invalid Token. Please Register or Login")
