import json
from http import HTTPStatus

from flask import Blueprint, request
from pydantic import ValidationError
from app.core.security import security

from app.ents.employee.crud import crud
from app.ents.employee.deps import authenticate, active_employee_required
from app.ents.employee.models import Employee
from app.ents.employee.schema import EmployeeCreateInput

from app.utilities.errors import MissingLoginCredentials, EmployeeDoesNotExist
from app.utilities.utils import (
    error_response,
    success_response,
    success_response_multi,
    validation_error_reponse,
)

bp = Blueprint("employees", __name__, url_prefix="/employees")


@bp.route("/", methods=["POST"])
def create_employee():
    """Create an employee."""
    try:
        data = json.loads(request.data)
        employee = crud.create(EmployeeCreateInput(**data))
        return success_response(data=employee, code=HTTPStatus.CREATED)
    except ValidationError as e:
        return validation_error_reponse(error=e, code=HTTPStatus.BAD_REQUEST)


@bp.route("/", methods=["GET"])
@active_employee_required
def get_employees(_: Employee):
    """Get all employees."""
    employees = crud.read_multi()
    return success_response_multi(data=employees, code=HTTPStatus.OK)


@bp.route("/<string:employee_id>", methods=["GET"])
def get_employee(employee_id: str):
    """Get an employee."""
    employee = crud.read(employee_id=employee_id)
    return (
        success_response(data=employee, code=HTTPStatus.OK)
        if employee
        else error_response(error="Employee does not exist.", code=HTTPStatus.NOT_FOUND)
    )


@bp.route("/login", methods=["POST"])
def login_employee():
    """Log in an employee."""
    form = request.form
    if not form or not form.get("email") or not form.get("password"):
        return error_response(error=MissingLoginCredentials.msg, code=HTTPStatus.UNAUTHORIZED)

    employee = authenticate(form.get("email"),form.get("password"))
    if employee:
        return success_response(data=security.create_token(employee), code=HTTPStatus.OK)
    return error_response(error=EmployeeDoesNotExist.msg, code=HTTPStatus.OK)

    