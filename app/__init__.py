import os
import secrets

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_login import LoginManager
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.orm import joinedload

from app.api import api_bp
from app.auth import auth_bp
from app.commands import db_cli_bp
from app.core import core_bp
from app.dashboard import dashboard_bp
from app.database import Users, db

load_dotenv()


def _get_bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    normalized = value.strip().lower()
    return normalized in {"1", "true", "yes", "on", "y"}


MAX_PROFILE_PICTURE_BYTES = 2 * 1024 * 1024

secret_key = os.getenv("SECRET_KEY")
if not secret_key:
    if os.getenv("FLASK_ENV") == "production":
        raise RuntimeError("SECRET_KEY is required in production mode.")
    secret_key = secrets.token_hex(32)

mail = Mail()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config["SECRET_KEY"] = secret_key
    app.secret_key = secret_key
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
    app.config["MAX_CONTENT_LENGTH"] = MAX_PROFILE_PICTURE_BYTES + 65536
    app.config["MAX_PROFILE_PICTURE_BYTES"] = MAX_PROFILE_PICTURE_BYTES
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = _get_bool_env("SESSION_COOKIE_SECURE", False)

    app.config["MAIL_SERVER"] = "mail.gmx.net"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USE_SSL"] = False
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_ADDRESS")

    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Users, int(user_id), options=[joinedload(Users.profile)])

    app.register_blueprint(core_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(db_cli_bp)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(error):
        if app.debug:
            raise error
        return render_template("404.html"), 500

    app.config["SERIALIZER"] = URLSafeTimedSerializer(secret_key)
    return app


__all__ = ["create_app", "_get_bool_env", "MAX_PROFILE_PICTURE_BYTES", "secret_key"]
