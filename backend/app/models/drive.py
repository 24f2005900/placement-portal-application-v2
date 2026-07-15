from datetime import datetime
from enum import Enum

from app.extensions import db


class DriveStatus(Enum):
    OPEN = "Open"
    CLOSED = "Closed"
    CANCELLED = "Cancelled"


class Drive(db.Model):
    __tablename__ = "drives"

    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(
        db.Integer,
        db.ForeignKey("companies.id"),
        nullable=False,
    )

    approved = db.Column(db.Boolean, default=False)

    title = db.Column(db.String(150), nullable=False)

    description = db.Column(db.Text)

    salary = db.Column(db.Integer)

    location = db.Column(db.String(120))

    eligibility = db.Column(db.Text)

    deadline = db.Column(db.Date)

    status = db.Column(
        db.Enum(DriveStatus),
        default=DriveStatus.OPEN,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
    )

    company = db.relationship("Company", back_populates="drives")

    applications = db.relationship(
        "Application",
        back_populates="drive",
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "company_id": self.company_id,
            "approved": self.approved,
            "title": self.title,
            "description": self.description,
            "salary": self.salary,
            "location": self.location,
            "eligibility": self.eligibility,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "status": self.status.value
        }