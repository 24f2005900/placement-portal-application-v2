from app.extensions import db


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False,
    )

    full_name = db.Column(db.String(120), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    department = db.Column(db.String(100))

    cgpa = db.Column(db.Float)

    skills = db.Column(db.Text)

    resume = db.Column(db.String(255))

    phone = db.Column(db.String(20))

    graduation_year = db.Column(db.Integer)

    user = db.relationship("User", back_populates="student")

    applications = db.relationship(
        "Application",
        back_populates="student",
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "full_name": self.full_name,
            "email": self.email,
            "department": self.department,
            "cgpa": self.cgpa,
            "skills": self.skills,
            "resume": self.resume,
            "phone": self.phone,
            "graduation_year": self.graduation_year
        }