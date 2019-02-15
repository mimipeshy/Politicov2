import os
import config
from flask import Flask

from config import app_config
from app.api.database.db_conn import create_tables
from app.api.routes.views.political import version2 as party



def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    with app.app_context():
        create_tables()
    app.register_blueprint(party)
    return app
