from app.ents.base.crud import db


class Employee(db.Model):  # type: ignore
    """Employees Table"""

    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String)
    first_name = db.Column(db.String)
    middle_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    full_name = db.Column(db.String)
    hashed_password = db.Column(db.String)
