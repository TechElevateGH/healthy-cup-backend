import json
from flask import Blueprint, request

from app.ents.employee.models import Employee
from app.ents.employee.schema import EmployeeOut, EmployeeIn

bp: Blueprint = Blueprint("employees", __name__, url_prefix="/employees")


@bp.route("/", methods=["POST"])
def create_employee():
    """Create an employees."""
    data: EmployeeIn = json.loads(request.data)
    employee = Employee.create(data)
    return employee.dict()


@bp.route("/", methods=["GET"])
def get_employees():
    """Get all employees."""
    employees: list[EmployeeOut] = Employee.read_multi()
    return [employee.dict() for employee in employees]


@bp.route("/<string:employee_id>", methods=["GET"])
def get_employee(employee_id: int):
    """Get an employees."""
    employee: EmployeeOut | None = Employee.read(employee_id=employee_id)
    return employee.dict() if employee else {}
