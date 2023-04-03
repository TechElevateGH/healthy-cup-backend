import json
from http import HTTPStatus

from datetime import datetime, timedelta, timezone

from flask import Blueprint, request
from pydantic import ValidationError

from app.core.security import security
from app.ents.base.deps import authenticate
from app.ents.employee.crud import crud
from app.ents.employee.schema import EmployeeCreateInput, EmployeeRead
from app.utilities.errors import EmployeeDoesNotExist, MissingLoginCredentials
from app.utilities.utils import (
    error_response,
    success_response,
    success_response_multi,
    validation_error_response,
)


from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import set_access_cookies


from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies


bp = Blueprint("employees", __name__, url_prefix="/employees")


@bp.route("/", methods=["POST"])
def create_employee():
    """Create an employee."""
    try:
        data = json.loads(request.data)
        employee = EmployeeCreateInput(**data)
        if crud.read_by_email(employee.email):
            return error_response(
                error="Employee with email already exists!",
                code=HTTPStatus.NOT_ACCEPTABLE,
            )
        return success_response(data=crud.create(employee), code=HTTPStatus.CREATED)
    except ValidationError as e:
        return validation_error_response(error=e, code=HTTPStatus.BAD_REQUEST)


@bp.route("/", methods=["GET"])
def get_employees():
    """Get all employees."""
    employees = [EmployeeRead(**employee.dict()) for employee in crud.read_multi()]
    return success_response_multi(data=employees, code=HTTPStatus.OK)


@bp.route("/<string:employee_id>", methods=["GET"])
def get_employee(employee_id: str):
    """Get employee with id `employee_id`."""
    employee = crud.read_by_id(employee_id=employee_id)
    return (
        success_response(data=EmployeeRead(**employee.dict()), code=HTTPStatus.OK)
        if employee
        else error_response(error="Employee does not exist.", code=HTTPStatus.NOT_FOUND)
    )


@bp.route("/login", methods=["POST"])
def login_employee():
    """Log in an employee."""
    form = request.form
    email, password = form.get("email"), form.get("password")

    if not form or not email or not password:
        return error_response(
            error=MissingLoginCredentials.msg, code=HTTPStatus.UNAUTHORIZED
        )

    employee = authenticate(crud, email, password)
    if employee:
        return success_response(
            data=EmployeeRead(**employee.dict()),
            code=HTTPStatus.OK,
            token=security.create_token(employee),
        )

    return error_response(error=EmployeeDoesNotExist.msg, code=HTTPStatus.BAD_REQUEST)


@bp.after_request
# @jwt_required
def refresh_expiring_jwts(success_response):
    try:
        employee_id = str(get_jwt_identity())
        if employee_id:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp >= exp_timestamp:
                token = security.create_token_with_id(employee_id)
                set_access_cookies(success_response, token)
        return success_response

    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return success_response
