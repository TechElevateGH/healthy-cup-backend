from typing import Optional
from app.ents.employee.schema import EmployeeIn, EmployeeOut
from flask_sqlalchemy import SQLAlchemy


db: SQLAlchemy = SQLAlchemy()


class Employee(db.Model):  # type: ignore
    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    middle_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)

    @classmethod
    def read(cls, employee_id: int) -> Optional[EmployeeOut]:
        """Read employee with id `employee_id`."""
        employee = cls.query.filter_by(id=employee_id).first()
        return EmployeeOut(**vars(employee)) if employee else None

    @classmethod
    def read_multi(cls) -> list[EmployeeOut]:
        """Read all employees."""
        employees = [EmployeeOut(**vars(employee)) for employee in cls.query.all()]
        return employees

    @classmethod
    def create(cls, data: EmployeeIn) -> EmployeeOut:
        """Create an employee with `data`."""
        employee = Employee(**data)

        db.session.add(employee)
        db.session.commit()
        db.session.refresh(employee)

        return EmployeeOut(**vars(employee))
