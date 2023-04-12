from flask import make_response
from pydantic import ValidationError


def success_response(*, data, code, token=""):
    return make_response(
        {"data": data.dict()}, code, {"Authorization": f"Bearer {token}"}
    )


def success_response_multi(*, data, code, token=""):
    return make_response(
        {"data": [item.dict() for item in data]},
        code,
        {"Authorization": f"Bearer {token}"},
    )


def validation_error_response(*, error: ValidationError, code):
    return make_response(
        {"errors": [{"field": e["loc"][0], "msg": e["msg"]} for e in error.errors()]},
        code,
    )


def error_response(*, error, code):
    return make_response({"errors": {"msg": error}}, code)
