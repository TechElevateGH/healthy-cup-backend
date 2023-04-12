from functools import wraps

from flask_jwt_extended import get_jwt_identity, jwt_required

from app.ents.admin.crud import crud as admin_crud
from app.utilities.reponses import error_response


def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user = admin_crud.read_by_email(admin_email=get_jwt_identity())

        if not user or user.role != "admin":
            return error_response(error="Admin required", code=403)

        return fn(*args, **kwargs)

    return wrapper
