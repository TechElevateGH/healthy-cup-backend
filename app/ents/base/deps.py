from functools import wraps

from app.core.security import security
from app.ents.employee.crud import EmployeeCRUD


def authenticate(crud: EmployeeCRUD, email: str, password: str):
    """Authenticates a user using `email` and `password`."""
    user = crud.read_by_email(email)  # type: ignore
    if not user:
        return None

    if security.verify_password(user.hashed_password, password):
        return user


def active_employee_required(crud, f):
    """Checks if the user is an active employee (authorized)."""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = security.verify_token()
        if type(token) == tuple:  # Invalid or Missing token
            return token

        employee = crud.read_by_email(token.get("public_id"))  # type: ignore
        return f(employee, *args, **kwargs)

    return decorated
