from functools import wraps

from app.core.security import security
from app.ents.employee.crud import crud

def active_employee_required(f):
    """Checks if the user is an active employee (authorized)."""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = security.verify_token()
        if type(token) == tuple: # Invalid or Missing token
            return  token

        employee = crud.read_by_email(token.get("public_id")) #type: ignore
        return f(employee, *args, **kwargs)

    return decorated




    