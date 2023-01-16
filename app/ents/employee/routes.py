import json
from flask import Blueprint, request
from pydantic import ValidationError

from app.ents.employee.crud import crud
from app.utils import (
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
        return success_response(data=employee, code=202)
    except ValidationError as e:
        return validation_error_reponse(error=e, code=400)


@bp.route("/", methods=["GET"])
def get_employees():
    """Get all employees."""
    employees = crud.read_multi()
    return success_response_multi(data=employees, code=200)


@bp.route("/<string:employee_id>", methods=["GET"])
def get_employee(employee_id: int):
    """Get an employees."""
    employee = crud.read(employee_id=employee_id)
    return (
        success_response(data=employee, code=200)
        if employee
        else not_exist_error_response(error="Employee does not exist.", code=404)
    )
