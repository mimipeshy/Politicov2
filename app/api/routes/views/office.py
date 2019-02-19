from os import abort

from flask import jsonify, request

from app.api.blueprints import version2
from app.api.responses import Responses
from app.api.routes.models.office import GovernmentOffice as ofisi
from app.api.routes.models.user import UserModel as u
from app.api.validations.utils import Validations


@version2.route("/office", methods=['POST'])
def create_an_office():
    """this creates a new office"""
    data = request.get_json()
    valid = Validations.create_office()
    if valid:
        return Validations.create_office()

    name = data['name']
    type = data['type']
    final = ofisi(name, type)
    response = final.add_political_office(name, type)
    result = [{"id": response[0], "name": response[1], "type": response[2]}]
    return jsonify({"msg": result}), 201


@version2.route("/office", methods=['GET'])
def get_all_offices():
    """this returns all offices"""

    return ofisi.get_all_offices()


@version2.route("/office/<int:id>", methods=['GET'])
def get_one_office(id):
    """this gets one specific office"""
    return ofisi.get_one_office(id)


# @version2.route("/office/<int:id>", methods=['GET'])
# def register_candidate_to_office(userobj, office_id):
#     """
#     this is where we check if the candidates information is
#     eligible so that it can be registered to an office.
#     """
#     try:
#         email = userobj[0][0]
#     except:
#         abort(Responses.bad_request("You don't have an account Create one"))
#
#     try:
#         data = request.get_json()
#         user = data["user"]
#
#     except KeyError:
#         abort(Responses.bad_request("User key should be present"))
#
#     # check if details are for an admin.
#     Validations.validate_admin(email)
#     # # check if fields are integers.
#     # utils.check_for_ints(data, ["user"])
#     # does the candidate & office exist in the db.
#     candidate = u.get_one_by_id(user_id)get_one_by_id(user)
#     office = OfficesModel.get_specific_office(office_id)
#     if candidate and office:
#         is_candidate_registered = CandidateModel.check_if_candidate_is_already_registered(
#             candidate[0][0], office[0]["id"])
#         if is_candidate_registered:
#             abort(utils.response_fn(400, "error",
#                                     "Candidate is already registered in this office"))
#
#         # register the politician user.to a certain office.
#         CandidateModel.register_politician_user_to_office(
#             office[0]["id"], candidate[0][0])
#         return utils.response_fn(201, "data", [{
#             "office": office[0]["id"],
#             "user": candidate[0][0]
#         }])
#     else:
#         return utils.response_fn(404, "error",
#                                  "Either candidate or office is missing in the database")