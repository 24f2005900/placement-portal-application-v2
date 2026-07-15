from datetime import datetime
from enum import Enum

from app.extensions import db


class ApplicationStatus(Enum):
    APPLIED = "Applied"
    SHORTLISTED = "Shortlisted"
    INTERVIEW = "Interview"
    SELECTED = "Selected"
    REJECTED = "Rejected"


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False,
    )

    drive_id = db.Column(
        db.Integer,
        db.ForeignKey("drives.id"),
        nullable=False,
    )

    status = db.Column(
        db.Enum(ApplicationStatus),
        default=ApplicationStatus.APPLIED,
    )

    remarks = db.Column(db.Text)

    applied_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
    )

    student = db.relationship(
        "Student",
        back_populates="applications",
    )

    drive = db.relationship(
        "Drive",
        back_populates="applications",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "drive_id": self.drive_id,
            "status": self.status.value,
            "remarks": self.remarks,
            "applied_at": self.applied_at.isoformat()
        }