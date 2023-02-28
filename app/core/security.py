from datetime import datetime, timedelta
from http import HTTPStatus

import jwt
from flask import request
from flask_bcrypt import Bcrypt  # type:ignore

from app.core.config import config
from app.utilities.errors import InvalidTokenError, MissingTokenError
from app.utilities.utils import error_response


class Security:
    bcrypt = Bcrypt()

    def hash_password(self, password: str) -> str:
        """Returns the hashed form of `password`."""
        return self.bcrypt.generate_password_hash(password.encode("utf-8"))  # type: ignore

    def verify_password(self, hashed_password: str, password: str) -> bool:
        """Returns `True` if `password` hashes to `hashed_password`."""
        return self.bcrypt.check_password_hash(hashed_password, password)

    def create_token(self, user):
        """Creates a JWT token with the `public_id` of the `user`."""
        token = jwt.encode(
            payload={
                "public_id": user.public_id,
                "expire_at": (datetime.utcnow() + timedelta(minutes=30)).ctime(),
            },
            key=config["SECRET_KEY"],  # type: ignore
            algorithm="HS256",
        )

        return token

    def verify_token(self):
        """Returns the decoded token in the request header (if valid)."""
        token = None

        token = request.headers.get("Authorization")
        if not token:
            return error_response(
                error=MissingTokenError.msg, code=HTTPStatus.UNAUTHORIZED
            )

        try:
            key = config.get("SECRET_KEY")
            decoded_token = jwt.decode(
                token, key=key if key else "", algorithms=["HS256"]
            )
            return decoded_token
        except:
            return error_response(
                error=InvalidTokenError.msg, code=HTTPStatus.UNAUTHORIZED
            )


security = Security()
