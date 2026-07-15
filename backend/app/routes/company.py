from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt

from app.extensions import db
from app.models import User, Company, Drive

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