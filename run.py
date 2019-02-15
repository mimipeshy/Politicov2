import os
from app.api.app import create_app
from flask import make_response, jsonify

from app.api.app import create_app

config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.errorhandler(404)
def error404(e):
    return make_response(jsonify({"Status": 404,
                                  "Data": "The requested URL is not found".format(e)}), 404)


@app.errorhandler(405)
def error405(e):
    return make_response(jsonify({"Status": 405,
                                  "Data": "The method is not allowed for the requested URL".format(e)}), 405)


@app.errorhandler(403)
def error403(e):
    return make_response(jsonify({"Status": 403,
                                  "Data": "This method is not allowed".format(e)}), 403)


@app.errorhandler(500)
def error500(e):
    return make_response(jsonify({"Status": 500,
                                  "Data": "Internal Server Error".format(e)}), 500)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run()
