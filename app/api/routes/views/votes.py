from flask import request, abort
from flask import request, jsonify, make_response

from app.api.blueprints import version2
from app.api.responses import Responses
from app.api.routes.models.office import GovernmentOffice as g
from app.api.routes.models.user import UserModel as u
from app.api.routes.models.votes import Vote as v
from app.api.validations.utils import Validations
from app.api.blueprints import version2


@version2.route("/votes", methods=['POST'])
def vote_for_office():
    """a user can vote once for an office"""
    try:
        data = request.get_json()
        office = data["office"]
        candidate = data["candidate"]
        voter = data["voter"]
    except Exception:
        return Responses.bad_request('Invalid your json keys. Use these keys '
                                     'office, candidate, voter ')
    if not isinstance(data['office'], str) or not isinstance(data['candidate'], str)or not isinstance(data["voter"], int):
        return Responses.bad_request('Incorrect input type'), 400

    vote = v(office, candidate, voter)
    vote.save_vote()
    return make_response(jsonify({"status": 201,
                                  "office": office,
                                  "candidate": candidate,
                                  "voter": voter}))

