import json
from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import set_refresh_cookies
from pydantic import ValidationError

from app.core.security import security
from app.ents.admin.deps import admin_required
from app.ents.base.deps import authenticate, is_active
from app.ents.employee.crud import crud as employee_crud
from app.ents.employee.schema import (EmployeeCreateInput, EmployeeLoginInput,
                                      EmployeeRead)
from app.utilities.errors import MissingLoginCredentials, UserDoesNotExist
from app.utilities.reponses import (error_response, success_response,
                                    success_response_multi,
                                    validation_error_response)

bp = Blueprint("employees", __name__, url_prefix="/employees")


@bp.route("/", methods=["POST"])
def create_employee():
    """Create an employee."""
    try:
        data = json.loads(request.data)
        employee = EmployeeCreateInput(**data)
        if employee_crud.read_by_email(employee.email):
            return error_response(
                error="Employee with email already exists!",
                code=HTTPStatus.NOT_ACCEPTABLE,
            )
        return success_response(
            data=employee_crud.create(employee), code=HTTPStatus.CREATED
        )
    except ValidationError as e:
        return validation_error_response(error=e, code=HTTPStatus.BAD_REQUEST)


@bp.route("/", methods=["GET"])
@admin_required
def get_employees():
    """Get all employees."""
    employees = [
        EmployeeRead(**employee.dict()) for employee in employee_crud.read_multi()
    ]
    return success_response_multi(data=employees, code=HTTPStatus.OK)


@bp.route("/<string:employee_id>", methods=["GET"])
def get_employee(employee_id: str):
    """Get employee with id `employee_id`."""
    employee = employee_crud.read_by_id(employee_id=employee_id)
    return (
        success_response(data=EmployeeRead(**employee.dict()), code=HTTPStatus.OK)
        if employee
        else error_response(error="Employee does not exist.", code=HTTPStatus.NOT_FOUND)
    )


@bp.route("/login", methods=["POST"])
@bp.route("/employees/login", methods=["POST"])
@bp.route("/clients/login", methods=["POST"])
def employee_client_login():
    """Log in an employee."""
    try:
        data = EmployeeLoginInput(**request.form)
        employee = is_active(authenticate(employee_crud, data.email, data.password))
        client = None

        if not (client or employee):
            return error_response(
                error=UserDoesNotExist.msg, code=HTTPStatus.BAD_REQUEST
            )

        response, tokens = None, ("", "")

        if employee and client:
            tokens = security.create_auth_tokens(employee.email)
            response = ...

        elif employee:
            tokens = security.create_auth_tokens(employee.email)
            response = EmployeeRead(**employee.dict())

        elif client:
            tokens = security.create_auth_tokens(client.email)
            response = ...

        set_refresh_cookies(response, tokens[1])
        return success_response(
            data=response,
            code=HTTPStatus.OK,
            token=tokens[0],
        )
    except ValidationError:
        return error_response(
            error=MissingLoginCredentials.msg, code=HTTPStatus.UNAUTHORIZED
        )


@bp.route("/<string:employee_id>", methods=["PUT"])
def update_employee(employee_id: str):
    return ""


# * Implement after SMTP integration
@bp.route("/<string:employee_id>/password-reset", methods=["POST"])
def reset_password(employee_id: str):
    return ""
