from flask import make_response
from pydantic import ValidationError


def success_response(*, data, code, headers: dict = {}, cookies: dict = {}):
    response = make_response({"data": data.dict()}, code)
    response.headers.extend(headers)

    for k, v in cookies.items():
        response.set_cookie(key=k, value=v)
    return response


def success_response_multi(*, data, code, headers={}, cookies={}):
    response = make_response({"data": [item.dict() for item in data]}, code)
    response.headers.extend(headers)

    for k, v in cookies.items():
        response.set_cookie(key=k, value=v)
    return response


def validation_error_response(*, error: ValidationError, code):
    return make_response(
        {"errors": [{"field": e["loc"][0], "msg": e["msg"]} for e in error.errors()]},
        code,
    )


def error_response(*, error, code):
    return make_response({"errors": {"msg": error}}, code)
