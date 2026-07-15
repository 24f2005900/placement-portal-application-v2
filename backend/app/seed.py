from app.extensions import db
from app.models import User, UserRole


def create_admin():
    admin = User.query.filter_by(username="admin").first()

    if admin:
        return

    admin = User(
        username="admin",
        role=UserRole.ADMIN
    )

    admin.set_password("admin123")

    db.session.add(admin)
    db.session.commit()

    print("Default admin created")