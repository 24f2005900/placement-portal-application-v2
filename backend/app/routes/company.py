from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt

from app.extensions import db
from app.models import User, Company, Drive
from app.models.application import Application, ApplicationStatus
from app.models.student import Student

company_bp = Blueprint("company", __name__, url_prefix="/api/company")


def get_company():
    claims = get_jwt()

    if claims["role"] != "company":
        return None

    user = User.query.get(int(claims["sub"]))

    if not user:
        return None

    return Company.query.filter_by(user_id=user.id).first()


@company_bp.get("/dashboard")
@jwt_required()
def dashboard():

    company = get_company()

    if not company:
        return jsonify({"message": "Unauthorized"}), 403

    drives = Drive.query.filter_by(company_id=company.id).all()

    return jsonify({
        "company": company.to_dict(),
        "total_drives": len(drives),
        "drives": [d.to_dict() for d in drives]
    })


@company_bp.post("/drive")
@jwt_required()
def create_drive():

    company = get_company()

    if not company:
        return jsonify({"message": "Unauthorized"}), 403

    if not company.approved:
        return jsonify({
            "message": "Company not approved by admin"
        }), 403

    data = request.get_json()

    drive = Drive(
        company_id=company.id,
        title=data["title"],
        description=data.get("description"),
        salary=data.get("salary"),
        location=data.get("location"),
        eligibility=data.get("eligibility"),
        deadline=datetime.strptime(
            data["deadline"],
            "%Y-%m-%d"
        ).date(),
    )

    db.session.add(drive)
    db.session.commit()

    return jsonify({
        "message": "Drive created and awaiting admin approval."
    })


@company_bp.get("/drives")
@jwt_required()
def drives():

    company = get_company()

    if not company:
        return jsonify([]), 403

    drives = Drive.query.filter_by(
        company_id=company.id
    ).all()

    return jsonify(
        [d.to_dict() for d in drives]
    )

@company_bp.get("/applications")
@jwt_required()
def view_applicants():

    company = get_company()

    if not company:
        return jsonify({"message": "Unauthorized"}), 403

    applications = (
        Application.query
        .join(Application.drive)
        .filter(Drive.company_id == company.id)
        .all()
    )

    result = []

    for application in applications:

        student = application.student
        drive = application.drive

        result.append({
            "application_id": application.id,
            "status": application.status.value,
            "applied_at": application.applied_at.isoformat(),

            "student": {
                "id": student.id,
                "full_name": student.full_name,
                "email": student.email,
                "department": student.department,
                "cgpa": student.cgpa,
                "skills": student.skills,
                "resume": student.resume,
                "phone": student.phone,
                "graduation_year": student.graduation_year,
            },

            "drive": {
                "id": drive.id,
                "title": drive.title
            }
        })

    return jsonify(result), 200

@company_bp.put("/applications/<int:application_id>")
@jwt_required()
def update_application_status(application_id):

    company = get_company()

    if not company:
        return jsonify({"message": "Unauthorized"}), 403

    application = (
        Application.query
        .join(Application.drive)
        .filter(
            Application.id == application_id,
            Drive.company_id == company.id
        )
        .first()
    )

    if not application:
        return jsonify({
            "message": "Application not found"
        }), 404

    data = request.get_json()

    status = data.get("status")
    remarks = data.get("remarks")

    if not status:
        return jsonify({
            "message": "Status is required"
        }), 400

    try:
        application.status = ApplicationStatus(status)
    except ValueError:
        return jsonify({
            "message": "Invalid application status"
        }), 400

    if remarks is not None:
        application.remarks = remarks

    db.session.commit()

    return jsonify({
        "message": "Application updated successfully",
        "application": application.to_dict()
    }), 200