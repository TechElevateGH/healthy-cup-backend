from functools import wraps

from flask_jwt_extended import get_jwt_identity, jwt_required

from app.ents.admin.models import Admin
from app.utilities.reponses import error_response


def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user = Admin.query.filter_by(id=get_jwt_identity()).first()

        if not user or user.role != "admin":
            return error_response(error="Admin required", code=403)

        return fn(*args, **kwargs)

    return wrapper
