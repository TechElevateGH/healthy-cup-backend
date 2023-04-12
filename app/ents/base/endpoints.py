from datetime import timedelta
from http import HTTPStatus

from flask import Blueprint
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                jwt_required)

from app.core.settings import settings
from app.utilities.errors import InvalidTokenError
from app.utilities.reponses import error_response

bp = Blueprint("/", __name__, url_prefix="/")


@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Refresh expired access token."""
    try:
        new_access_token = create_access_token(
            str(get_jwt_identity()),
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        return (
            {"data": "Success, Token refreshed!"},
            HTTPStatus.OK,
            {"Authorization": f"Bearer {new_access_token}"},
        )
    except (RuntimeError, KeyError):
        return error_response(error=InvalidTokenError.msg, code=HTTPStatus.BAD_REQUEST)
