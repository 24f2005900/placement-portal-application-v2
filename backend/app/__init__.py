from flask import Flask
from flask_cors import CORS

from .config import Config
from .extensions import db
from .extensions import jwt
from .extensions import migrate
from .extensions import bcrypt
from app.models import *
from app.routes.auth import auth_bp
from app.routes.admin import admin_bp
from app.routes.company import company_bp
from app.routes.student import student_bp

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)

    jwt.init_app(app)

    migrate.init_app(app, db)

    bcrypt.init_app(app)

    from app.seed import create_admin

    with app.app_context():
        create_admin()

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(student_bp)
    
    return app