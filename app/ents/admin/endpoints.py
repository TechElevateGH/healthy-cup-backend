import json
from http import HTTPStatus

from flask import Blueprint, request
from pydantic import ValidationError

from app.core.security import security
from app.ents.admin.crud import crud as admin_crud
from app.ents.admin.deps import admin_required
from app.ents.admin.schema import AdminCreateInput, AdminLoginInput, AdminRead
from app.ents.base.deps import authenticate, is_active
from app.utilities.errors import MissingLoginCredentials, UserDoesNotExist
from app.utilities.reponses import (error_response, success_response,
                                    success_response_multi,
                                    validation_error_response)

bp = Blueprint("admins", __name__, url_prefix="/admins")


@bp.route("/<string:admin_id>/", methods=["GET"])
def get(admin_id: str):
    admin = admin_crud.read_by_id(admin_id=admin_id)
    return (
        success_response(data=AdminRead(**vars(admin)), code=HTTPStatus.OK)
        if admin
        else error_response(error="Admin does not exist.", code=HTTPStatus.NOT_FOUND)
    )


@bp.route("/login", methods=["POST"])
def login():
    try:
        data = AdminLoginInput.parse_obj(request.form)
        admin = is_active(authenticate(admin_crud, data.email, data.password))
        if admin:
            tokens = security.create_auth_tokens(admin.email)
            return success_response(
                data=AdminRead(**vars(admin)),
                code=HTTPStatus.OK,
                headers={"Authorization": f"Bearer {tokens[0]}"},
                cookies={"refresh_token": f"Bearer {tokens[1]}"},
            )

        return error_response(error=UserDoesNotExist.msg, code=HTTPStatus.BAD_REQUEST)
    except ValidationError:
        return error_response(
            error=MissingLoginCredentials.msg, code=HTTPStatus.UNAUTHORIZED
        )


@bp.route("/", methods=["GET"])
@admin_required
def get_admins():
    admins = [AdminRead.parse_obj(admin) for admin in admin_crud.read_multi()]
    return success_response_multi(data=admins, code=HTTPStatus.OK)


@bp.route("/", methods=["POST"])
def create_admin():
    try:
        data = json.loads(request.data)
        admin = AdminCreateInput.parse_obj(data)
        if admin_crud.read_by_email(admin.email):
            return error_response(
                error="Admin with email already exists!",
                code=HTTPStatus.NOT_ACCEPTABLE,
            )
        return success_response(data=admin_crud.create(admin), code=HTTPStatus.CREATED)
    except ValidationError as e:
        return validation_error_response(error=e, code=HTTPStatus.BAD_REQUEST)
