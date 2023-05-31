import json
from http import HTTPStatus

from flask import Blueprint, request
from pydantic import ValidationError

from app.core.security import security
from app.ents.admin.deps import admin_required
from app.ents.base.deps import authenticate, is_active
from app.ents.client.crud import crud as client_crud
from app.ents.client.schema import (ClientCreateInput, ClientLoginInput, ClientReadClient)
from app.utilities.errors import MissingLoginCredentials, UserDoesNotExist
from app.utilities.reponses import (error_response, success_response,
                                    success_response_multi,
                                    validation_error_response)

bp = Blueprint("clients", __name__, url_prefix="/clients")

@bp.post("/")
def create_client():
    """Create a client"""
    try:
        data = json.loads(request.data)
        client = ClientCreateInput(**data)
        if client_crud.read_by_email(client.email):
            return error_response(
                error="Client with email already exists!",
                code=HTTPStatus.NOT_ACCEPTABLE,
            )
        new_client = client_crud.create(client)

        return success_response(
            data=ClientReadClient(**vars(new_client)),
            code=HTTPStatus.CREATED,
        )
    except ValidationError as e:
        return validation_error_response(error=e, code=HTTPStatus.BAD_REQUEST)


@bp.get("/")
@admin_required
def get_clients():
    clients = [
        ClientReadClient(**vars(client))
        for client in client_crud.read_multi()
    ]
    return success_response_multi(data=clients, code=HTTPStatus.OK)


@bp.get("/<str:client_id>")
def get_client(client_id: str):
    """Returns client with id `client_id`."""
    client = client_crud.read_by_id(client_id=client_id)
    return (
        success_response(
            data=ClientReadClient.parse_obj(client), code=HTTPStatus.OK
        )
        if client
        else error_response(error="Client does not exist.", code=HTTPStatus.NOT_FOUND)
    )


@bp.post("/clients/login")
def employee_client_login():
    """Log in a client."""
    try:
        data = ClientLoginInput.parse_obj(request.form)
        client = is_active(authenticate(client_crud, data.email, data.password))
    

        if not (client):
            return error_response(
                error=UserDoesNotExist.msg, code=HTTPStatus.BAD_REQUEST
            )

        response, tokens = None, ("", "")

        if client:
            tokens = security.create_auth_tokens(client.email)
            response = ...

        return success_response(
            data=response,
            code=HTTPStatus.OK,
            headers={"Authorization": f"Bearer {tokens[0]}"},
            cookies={"refresh_token": f"Bearer {tokens[1]}"},
        )
    except ValidationError:
        return error_response(
            error=MissingLoginCredentials.msg, code=HTTPStatus.UNAUTHORIZED
        )


@bp.put("/<str:client_id>")
def update_client(client_id: str):
    return ""


@bp.post("/<str:client_id>")
def reset_password(client_id: str):
    return ""
