from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from app.extensions import db
from app.models import Student, Company, Drive, Application

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


def admin_required():
    claims = get_jwt()
    return claims["role"] == "admin"


@admin_bp.get("/dashboard")
@jwt_required()
def dashboard():

    if not admin_required():
        return jsonify({"message": "Forbidden"}), 403

    return jsonify({
        "students": Student.query.count(),
        "companies": Company.query.count(),
        "drives": Drive.query.count(),
        "applications": Application.query.count()
    })


@admin_bp.get("/companies")
@jwt_required()
def companies():

    if not admin_required():
        return jsonify({"companies": []}), 403

    companies = Company.query.all()

    return jsonify([c.to_dict() for c in companies])


@admin_bp.get("/students")
@jwt_required()
def students():

    if not admin_required():
        return jsonify([]), 403

    students = Student.query.all()

    return jsonify([s.to_dict() for s in students])