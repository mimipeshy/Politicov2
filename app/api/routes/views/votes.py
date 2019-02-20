from flask import request

from app.api.blueprints import version2
from app.api.routes.models.votes import Vote as v


@version2.route("/votes", methods=['POST'])
# @jwt_required
def vote_for_office():
    """a user can vote once for an office"""
    data = request.get_json()
    # if not data:
    #     return Responses.bad_request('Invalid your json keys. Use these keys '
    #                                  'office, candidate, voter ')
    # if not isinstance(data['office'], int) or not isinstance(data['candidate'],int)or not isinstance(data["voter"], int):
    #     return Responses.bad_request('Incorrect input type'), 400
    office = data["office"]
    candidate = data["candidate"]
    voter = data["voter"]
    vote = v(office, candidate, voter)
    res= vote.save_vote()
    return res
