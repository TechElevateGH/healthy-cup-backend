from sqlalchemy import Boolean, Column, Integer, String

from app.ents.base.crud import db


class Admin(db.Model):  # type: ignore
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    email = Column(String)
    username = Column(String)
    password = Column(String)
    role = Column(String)
    active = Column(Boolean)

    def __init__(
        self, email: str, username: str, password: str, role: str, active: bool
    ) -> None:
        self.email = email
        self.username = username
        self.password = password
        self.role = role
        self.active = active
