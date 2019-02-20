import os
import config
from flask import Flask
from flask_jwt_extended import JWTManager
from config import app_config
from app.api.database.db_conn import create_tables
from app.api.routes.views.political import version2 as party
from app.api.routes.views.office import version2 as office
from app.api.routes.views.auth import version2 as auth
from app.api.routes.views.votes import version2 as votes



def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    jwt = JWTManager(app)
    app.config.from_object(app_config[config_name])
    with app.app_context():
        create_tables()
    app.register_blueprint(party)
    app.register_blueprint(office)
    app.register_blueprint(auth)
    app.register_blueprint(votes)
    return app
