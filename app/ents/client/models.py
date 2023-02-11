from sqlalchemy import Boolean, Column, Integer, String

from app.ents.base.crud import db


class Client(db.Model):
    """Clients Table"""

    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    full_name = Column(String)
    email = Column(String)
    password = Column(String)
    company = Column(String)
    active = Column(Boolean)

    def __init__(
        self,
        first_name: str,
        middle_name: str,
        last_name: str,
        full_name: str,
        email: str,
        password: str,
        company: str,
        active: bool,

    ) -> None:
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.full_name = full_name
        self.email = email
        self.password = password
        self.company = company
        self.active = active