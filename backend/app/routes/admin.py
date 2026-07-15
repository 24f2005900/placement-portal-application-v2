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

    query = Company.query

    approved = request.args.get("approved")
    name = request.args.get("name")

    if approved is not None:
        query = query.filter(
            Company.approved == (
                approved.lower() == "true"
            )
        )

    if name:
        query = query.filter(
            Company.company_name.ilike(f"%{name}%")
        )

    companies = query.all()

    return jsonify([c.to_dict() for c in companies])


@admin_bp.get("/students")
@jwt_required()
def students():

    if not admin_required():
        return jsonify([]), 403

    students = Student.query.all()

    return jsonify([s.to_dict() for s in students])

@admin_bp.put("/company/<int:company_id>/approve")
@jwt_required()
def approve_company(company_id):

    if not admin_required():
        return jsonify({"message": "Forbidden"}), 403

    company = Company.query.get_or_404(company_id)

    company.approved = True

    db.session.commit()

    return jsonify({"message": "Company approved"})

@admin_bp.put("/company/<int:company_id>/blacklist")
@jwt_required()
def blacklist_company(company_id):

    if not admin_required():
        return jsonify({"message": "Forbidden"}), 403

    company = Company.query.get_or_404(company_id)

    company.blacklisted = True

    db.session.commit()

    return jsonify({"message": "Company blacklisted"})

@admin_bp.put("/drive/<int:drive_id>/approve")
@jwt_required()
def approve_drive(drive_id):

    if not admin_required():
        return jsonify({"message": "Forbidden"}), 403

    drive = Drive.query.get_or_404(drive_id)

    drive.approved = True

    db.session.commit()

    return jsonify({"message": "Drive approved"})

@admin_bp.put("/student/<int:student_id>/deactivate")
@jwt_required()
def deactivate_student(student_id):

    if not admin_required():
        return jsonify({"message": "Forbidden"}), 403

    student = Student.query.get_or_404(student_id)

    student.user.is_active = False

    db.session.commit()

    return jsonify({"message": "Student deactivated"})