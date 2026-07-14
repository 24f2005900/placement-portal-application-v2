from flask import Flask

from .config import Config
from .extensions import db
from .extensions import jwt
from .extensions import migrate
from .extensions import bcrypt

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    jwt.init_app(app)

    migrate.init_app(app, db)

    bcrypt.init_app(app)

    return app