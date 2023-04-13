# from functools import wraps

from app.core.security import security


def authenticate(crud, email: str, password: str):
    """Authenticates a user using `email` and `password`."""
    user = crud.read_by_email(email)  # type: ignore
    if not user:
        return None

    if security.verify_password(user.password, password):
        return user


def is_active(user):
    return None if not user else (user if user.active else None)


# def active_employee_required(crud, f):
#     """Checks if the user is an active employee (authorized)."""

#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = security.verify_token()
#         if type(token) == tuple:  # Invalid or Missing token
#             return token

#         employee = crud.read_by_email(token.get("public_id"))  # type: ignore
#         return f(employee, *args, **kwargs)

#     return decorated
