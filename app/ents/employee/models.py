from sqlalchemy import Boolean, Column, Integer, String

from app.ents.base.crud import db


class Employee(db.Model):  # type: ignore
    """Employees Table"""

    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    full_name = Column(String)
    password = Column(String)
    is_supervisor = Column(Boolean)
    role = Column(String)

    def __init__(
        self,
        first_name: str,
        middle_name: str,
        last_name: str,
        email: str,
        full_name: str,
        password: str,
    ) -> None:
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.email = email
        self.full_name = full_name
        self.password = password
