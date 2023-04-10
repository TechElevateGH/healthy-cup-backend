import json
from datetime import datetime, timedelta, timezone
from http import HTTPStatus

from flask import Blueprint, request, make_response
from flask_jwt_extended import (get_jwt, get_jwt_identity, jwt_required,
                                set_access_cookies, set_refresh_cookies,
                                create_access_token, create_refresh_token)
from pydantic import ValidationError

from app.core.security import security
from app.core.settings import settings
from app.ents.base.deps import authenticate
from app.ents.employee.crud import crud
from app.ents.employee.schema import EmployeeCreateInput, EmployeeRead
from app.utilities.errors import EmployeeDoesNotExist, MissingLoginCredentials
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
        if crud.read_by_email(employee.email):
            return error_response(
                error="Employee with email already exists!",
                code=HTTPStatus.NOT_ACCEPTABLE,
            )
        return success_response(data=crud.create(employee), code=HTTPStatus.CREATED)
    except ValidationError as e:
        return validation_error_response(error=e, code=HTTPStatus.BAD_REQUEST)


@bp.route("/", methods=["GET"])
@jwt_required()
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

    if not (form and email and password):
        return error_response(
            error=MissingLoginCredentials.msg, code=HTTPStatus.UNAUTHORIZED
        )

    employee = authenticate(crud, email, password)
    if employee:
        access_token = create_access_token(employee.id, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        refresh_token = create_refresh_token(employee.id, expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES))

        resp= success_response(
            data=EmployeeRead(**employee.dict()),
            code=HTTPStatus.OK,
            token=access_token,
        )
        response = make_response(resp)

        set_refresh_cookies(response, refresh_token)

        return response

    return error_response(error=EmployeeDoesNotExist.msg, code=HTTPStatus.BAD_REQUEST)


@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    try:
        employee_id = str(get_jwt_identity())
        new_access_token = create_access_token(employee_id, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        employee = crud.read_by_id(employee_id=employee_id)
        if employee:
            return success_response(
                data=EmployeeRead(**employee.dict()),
                code=HTTPStatus.OK,
                token=new_access_token,
            )
               
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return error_response(error=EmployeeDoesNotExist.msg, code=HTTPStatus.BAD_REQUEST)
        


