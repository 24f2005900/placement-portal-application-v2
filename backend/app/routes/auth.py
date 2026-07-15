from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt


from app.extensions import db
from app.models import User, UserRole, Student, Company

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.post("/register/student")
def register_student():

    data = request.get_json()

    if User.query.filter_by(username=data["email"]).first():
        return jsonify({"message": "Email already exists"}), 400

    user = User(
        username=data["email"],
        role=UserRole.STUDENT
    )

    user.set_password(data["password"])

    db.session.add(user)
    db.session.flush()

    student = Student(
        user_id=user.id,
        full_name=data["full_name"],
        email=data["email"],
        department=data.get("department"),
        cgpa=data.get("cgpa"),
        skills=data.get("skills"),
        phone=data.get("phone"),
        graduation_year=data.get("graduation_year")
    )

    db.session.add(student)

    db.session.commit()

    return jsonify({
        "message": "Student registered successfully"
    }), 201

@auth_bp.post("/register/company")
def register_company():

    data = request.get_json()

    if User.query.filter_by(username=data["hr_email"]).first():
        return jsonify({"message": "Email already exists"}), 400

    user = User(
        username=data["hr_email"],
        role=UserRole.COMPANY
    )

    user.set_password(data["password"])

    db.session.add(user)
    db.session.flush()

    company = Company(
        user_id=user.id,
        company_name=data["company_name"],
        hr_email=data["hr_email"],
        website=data.get("website"),
        description=data.get("description")
    )

    db.session.add(company)

    db.session.commit()

    return jsonify({
        "message": "Company registered. Awaiting admin approval."
    }), 201

@auth_bp.post("/login")
def login():

    data = request.get_json()

    user = User.query.filter_by(
        username=data["email"]
    ).first()

    if not user:
        return jsonify({
            "message": "Invalid credentials"
        }), 401

    if not user.check_password(data["password"]):
        return jsonify({
            "message": "Invalid credentials"
        }), 401

    if not user.is_active:
        return jsonify({
            "message": "Account deactivated"
        }), 403

    if user.role == UserRole.COMPANY:

        company = Company.query.filter_by(user_id=user.id).first()

        if not company.approved:

            return jsonify({
                "message": "Company not approved yet"
            }), 403

    token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role.value
        }
    )

    return jsonify({
        "token": token,
        "role": user.role.value
    })

@auth_bp.get("/me")
@jwt_required()
def me():

    claims = get_jwt()

    return jsonify({
        "message": "Authenticated",
        "role": claims["role"]
    })