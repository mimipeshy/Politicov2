import os
import config
from flask import Flask

from config import app_config
from app.api.database.db_conn import create_tables
from app.api.routes.views.political import version2 as party
from app.api.routes.views.office import version2 as office
from app.api.routes.views.auth import version2 as auth
from app.api.routes.views.votes import version2 as votes

from flask_jwt_extended import JWTManager


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    with app.app_context():
        create_tables()
    app.register_blueprint(party)
    app.register_blueprint(office)
    app.register_blueprint(auth)
    app.register_blueprint(votes)

    JWTManager(app)
    return app
