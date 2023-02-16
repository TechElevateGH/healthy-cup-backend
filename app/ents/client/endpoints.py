import json
from http import HTTPStatus

from flask import Blueprint, request
from pydantic import ValidationError

bp = Blueprint("clients", __name__, url_prefix="/clients")

from app.core.security import security
from app.ents.client.crud import crud as client_crud
from app.ents.client.schema import (ClientCreateInput, ClientLoginInput, ClientReadClient)
from app.utilities.reponses import (error_response, success_response,
                                    success_response_multi,
                                    validation_error_response)


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
def get_clients():
    """Get all clients"""
    return


@bp.get("/<str:client_id>")
def get_client(client_id):
    client = ...
    return 


@bp.put("/<str:client_id>")
def update_client(client_id):
    return ""


@bp.post("/<str:client_id>")
def reset_password(client_id):
    return ""
