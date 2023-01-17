import json
from http import HTTPStatus

from flask import Blueprint, request
from pydantic import ValidationError

from app.ents.employee.crud import crud
from app.utilities.utils import (
    not_exist_error_response,
    success_response,
    success_response_multi,
    validation_error_reponse,
)

bp: Blueprint = Blueprint("employees", __name__, url_prefix="/employees")


@bp.route("/", methods=["POST"])
def create_employee():
    """Create an employee."""
    try:
        data = json.loads(request.data)
        employee = crud.create(data)
        return success_response(data=employee, code=HTTPStatus.OK)
    except ValidationError as e:
        return validation_error_reponse(error=e, code=HTTPStatus.BAD_REQUEST)


@bp.route("/", methods=["GET"])
def get_employees():
    """Get all employees."""
    employees = crud.read_multi()
    return success_response_multi(data=employees, code=HTTPStatus.OK)


@bp.route("/<string:employee_id>", methods=["GET"])
def get_employee(employee_id: int):
    """Get an employees."""
    employee = crud.read(employee_id=employee_id)
    return (
        success_response(data=employee, code=HTTPStatus.OK)
        if employee
        else not_exist_error_response(
            error="Employee does not exist.", code=HTTPStatus.NOT_FOUND
        )
    )
