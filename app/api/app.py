import os
import config
from flask import Flask

from config import app_config
from app.api.database.db_conn import create_tables



def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    with app.app_context():
        create_tables()
    return app
