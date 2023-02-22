import json
from http import HTTPStatus

from flask import Blueprint, request
from pydantic import ValidationError
from app.core.security import security
from app.ents.base.deps import authenticate

from app.ents.employee.crud import crud
from app.ents.employee.deps import  active_employee_required
from app.ents.employee.models import Employee
from app.ents.employee.schema import EmployeeCreateInput, EmployeeRead

from app.utilities.errors import MissingLoginCredentials, EmployeeDoesNotExist
from app.utilities.utils import (
    error_response,
    success_response,
    success_response_multi,
    validation_error_response,
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
        return validation_error_response(error=e, code=HTTPStatus.BAD_REQUEST)


@bp.route("/", methods=["GET"])
@active_employee_required
def get_employees(_: Employee):
    """Get all employees."""
    employees = crud.read_multi()
    return success_response_multi(data=employees, code=HTTPStatus.OK)


@bp.route("/<string:employee_id>", methods=["GET"])
def get_employee(employee_id: str):
    """Get employee with id `employee_id`."""
    employee = crud.read_by_id(employee_id=employee_id)
    return (
        success_response(data=employee, code=HTTPStatus.OK)
        if employee
        else error_response(error="Employee does not exist.", code=HTTPStatus.NOT_FOUND)
    )


@bp.route("/login", methods=["POST"])
def login_employee():
    """Log in an employee."""
    form = request.form
    email, password = form.get("email"), form.get("password")

    if not form or not email or not password:
        return error_response(error=MissingLoginCredentials.msg, code=HTTPStatus.UNAUTHORIZED)

    employee = authenticate(crud, email,password)
    if employee:
        return success_response(
            data=EmployeeRead(**employee.dict()), 
            code=HTTPStatus.OK, 
            token=security.create_token(employee))

    return error_response(error=EmployeeDoesNotExist.msg, code=HTTPStatus.OK)

    