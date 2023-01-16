def success_response(*, data, code):
    return {"data": data.dict()}, code


def success_response_multi(*, data, code):
    return {"data": [item.dict() for item in data]}, code


def validation_error_reponse(*, error, code):
    return {
        "errors": [{"field": e["loc"][0], "msg": e["msg"]} for e in error.errors()]
    }, code


def not_exist_error_response(*, error, code):
    return {"errors": error}, code
