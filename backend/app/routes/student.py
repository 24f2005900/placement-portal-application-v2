from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt

from app.extensions import db
from app.models import User, Student, Drive, Application

student_bp = Blueprint(
    "student",
    __name__,
    url_prefix="/api/student"
)


def get_student():

    claims = get_jwt()

    if claims["role"] != "student":
        return None

    user = db.session.get(User, int(claims["sub"]))

    return Student.query.filter_by(
        user_id=user.id
    ).first()


@student_bp.get("/dashboard")
@jwt_required()
def dashboard():

    student = get_student()

    drives = Drive.query.filter_by(
        approved=True
    ).all()

    return jsonify({
        "student": student.to_dict(),
        "drives": [d.to_dict() for d in drives]
    })


@student_bp.post("/apply/<int:drive_id>")
@jwt_required()
def apply(drive_id):

    student = get_student()

    existing = Application.query.filter_by(
        student_id=student.id,
        drive_id=drive_id
    ).first()

    if existing:

        return jsonify({
            "message": "Already applied."
        }), 400

    application = Application(
        student_id=student.id,
        drive_id=drive_id
    )

    db.session.add(application)

    db.session.commit()

    return jsonify({
        "message": "Application submitted."
    })


@student_bp.get("/applications")
@jwt_required()
def applications():

    student = get_student()

    apps = Application.query.filter_by(
        student_id=student.id
    ).all()

    return jsonify(
        [a.to_dict() for a in apps]
    )


@student_bp.put("/profile")
@jwt_required()
def update_profile():

    student = get_student()

    data = request.get_json()

    student.skills = data.get(
        "skills",
        student.skills
    )

    student.cgpa = data.get(
        "cgpa",
        student.cgpa
    )

    student.phone = data.get(
        "phone",
        student.phone
    )

    db.session.commit()

    return jsonify(student.to_dict())