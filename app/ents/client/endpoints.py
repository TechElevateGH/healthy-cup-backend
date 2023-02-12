import json
from flask import Blueprint

bp = Blueprint("clients", __name__, url_prefix="/clients")

from app.core.security import security

@bp.post("/")
def create_client():
    """Create a client"""
    try:
        pass
    except:
        pass


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
