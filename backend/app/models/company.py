from app.extensions import db


class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False,
    )

    company_name = db.Column(db.String(150), nullable=False)

    website = db.Column(db.String(255))

    description = db.Column(db.Text)

    hr_email = db.Column(db.String(120))

    approved = db.Column(db.Boolean, default=False)

    blacklisted = db.Column(db.Boolean, default=False)

    user = db.relationship("User", back_populates="company")

    drives = db.relationship(
        "Drive",
        back_populates="company",
        cascade="all, delete-orphan",
    )
    
    def to_dict(self):
        return {
            "id": self.id,
            "company_name": self.company_name,
            "website": self.website,
            "description": self.description,
            "hr_email": self.hr_email,
            "approved": self.approved,
            "blacklisted": self.blacklisted
        }