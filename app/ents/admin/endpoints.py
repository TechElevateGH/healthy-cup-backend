import json
from http import HTTPStatus

from flask import Blueprint, request
from flask_restful import Api, Resource
from pydantic import ValidationError

from app.core.security import security
from app.ents.admin.crud import crud as admin_crud
from app.ents.admin.deps import admin_required
from app.ents.admin.schema import AdminCreateInput, AdminLoginInput, AdminRead
from app.ents.base.deps import authenticate, is_active
from app.utilities.errors import MissingLoginCredentials, UserDoesNotExist
from app.utilities.reponses import (
    error_response,
    success_response,
    success_response_multi,
    validation_error_response,
)

bp = Blueprint("admins", __name__, url_prefix="/admins")
api = Api(bp)


class AdminEndpoint(Resource):
    def get(self, admin_id: str):
        """Get admin with id `admin_id`."""
        admin = admin_crud.read_by_id(admin_id=admin_id)
        return (
            success_response(data=AdminRead.parse_obj(admin), code=HTTPStatus.OK)
            if admin
            else error_response(
                error="Admin does not exist.", code=HTTPStatus.NOT_FOUND
            )
        )


class AdminLoginEndpoint(Resource):
    def post(self):
        """Log in an admin."""
        try:
            data = AdminLoginInput.parse_obj(request.form)
            admin = is_active(authenticate(admin_crud, data.email, data.password))
            if admin:
                tokens = security.create_auth_tokens(admin.email)
                return success_response(
                    data=AdminRead(**admin.dict()),
                    code=HTTPStatus.OK,
                    headers={"Authorization": f"Bearer {tokens[0]}"},
                    cookies={"refresh_token": f"Bearer {tokens[1]}"},
                )

            return error_response(
                error=UserDoesNotExist.msg, code=HTTPStatus.BAD_REQUEST
            )
        except ValidationError:
            return error_response(
                error=MissingLoginCredentials.msg, code=HTTPStatus.UNAUTHORIZED
            )


class AdminsEndpoint(Resource):
    @admin_required
    def get(self):
        """Get all admins."""
        admins = [AdminRead.parse_obj(admin) for admin in admin_crud.read_multi()]
        return success_response_multi(data=admins, code=HTTPStatus.OK)

    def post(self):
        """Create an admin."""
        try:
            data = json.loads(request.data)
            admin = AdminCreateInput.parse_obj(data)
            if admin_crud.read_by_email(admin.email):
                return error_response(
                    error="Admin with email already exists!",
                    code=HTTPStatus.NOT_ACCEPTABLE,
                )
            return success_response(
                data=admin_crud.create(admin), code=HTTPStatus.CREATED
            )
        except ValidationError as e:
            return validation_error_response(error=e, code=HTTPStatus.BAD_REQUEST)


api.add_resource(AdminEndpoint, "/<string:admin_id>/")
api.add_resource(AdminsEndpoint, "/")
api.add_resource(AdminLoginEndpoint, "/login")
