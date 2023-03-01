import uuid
from app.ents.base.crud import db
from sqlalchemy.dialects.postgresql import UUID

class Employee(db.Model):  # type: ignore
    """Employees Table"""

    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    middle_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    full_name = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self,  first_name: str, middle_name: str, last_name: str, email: str, full_name: str, password: str) -> None:
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.email = email
        self.full_name = full_name
        self.password = password
