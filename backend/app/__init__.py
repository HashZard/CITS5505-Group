import os
import secrets

from flask import Flask, request
from dotenv import load_dotenv

from backend.app.models import db, init_db

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

env = os.getenv("FLASK_ENV", "development")
env_file = os.path.join(project_root, f".env.{env}" if env != "development" else ".env")
load_dotenv(env_file)


def create_app():
    app = Flask(__name__)

    # 初始化日志
    loggers = setup_logger()
    app_logger = loggers['app_logger']

    @app.before_request
    def before_request():
        app_logger.info(f"Request: {request.method} {request.path}"
                        + f" with data: {request.get_json(silent=True)}")

    @app.after_request
    def after_request(response):
        app_logger.info(f"Response: {response.status}"
                        + f" with data: {response.get_json(silent=True)}")
        return response

    # database config
    BACKEND_ROOT = os.path.dirname(os.path.dirname(__file__))
    DATABASE_PATH = os.path.join(BACKEND_ROOT, os.getenv("DATABASE_NAME"))
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DATABASE_PATH}"
    app.config['TESTING'] = os.getenv("FLASK_ENV") == "test"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # initialize database
    init_db(app)
    print("Database initialized.")

    # register Blueprint
    from backend.app.routes.auth_router import auth_bp
    from backend.app.routes.course_router import course_bp
    from backend.app.routes.instructor_router import instructor_bp
    from backend.app.routes.user_router import user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(instructor_bp)
    app.register_blueprint(user_bp)

    print("✅ Current all app routes:")
    for rule in app.url_map.iter_rules():
        print("➡", rule)

    # setting CSRF protection
    app.secret_key = secrets.token_hex(32)

    return app


import logging
from logging.handlers import RotatingFileHandler

log_dir = os.path.join(project_root, "logs")


def setup_logger():
    loggers = {
        'app_logger': create_logger('app_logger', os.path.join(log_dir, "app.log"), logging.DEBUG),
        'db_logger': create_logger('db_logger', os.path.join(log_dir, "db.log"), logging.INFO)
    }

    return loggers


def create_logger(logger_name, log_file, log_level):
    # create logs directory if not exists
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s [%(filename)s:%(lineno)d]: %(message)s'
    )

    file_handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    # create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    # create logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # set to DEBUG to capture all levels
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.propagate = False

    return logger
