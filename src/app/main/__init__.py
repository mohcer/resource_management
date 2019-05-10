from flask import Flask
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from logging.handlers import RotatingFileHandler
from .config import config_by_name

import logging

app = Flask(__name__)

db = SQLAlchemy()
flask_bcrypt = Bcrypt()


def get_log_handler():
    """
    :return None:
    purpose: Configures and Initializes the logger
    """
    global app

    log_file_loc = app.config['LOG_FILE_LOCATION'] + 'app.log'
    log_format = '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    rthandler = RotatingFileHandler(log_file_loc, maxBytes=20000, backupCount=0)
    rthandler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(log_format)
    rthandler.setFormatter(formatter)

    return rthandler


def create_app(config_name):
    global app
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    flask_bcrypt.init_app(app)

    log_handler = get_log_handler()

    app.logger.addHandler(log_handler)

    app.logger.info("****** App created successfully!! ******")
    app.logger.debug("Debug message")

    return app

