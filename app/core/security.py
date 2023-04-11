from datetime import timedelta

from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token

from app.core.settings import settings


class Security:
    bcrypt = Bcrypt()

    def hash_password(self, password: str) -> str:
        """Returns the hashed form of `password`."""
        return self.bcrypt.generate_password_hash(password.encode("utf-8"))  # type: ignore

    def verify_password(self, hashed_password: str, password: str) -> bool:
        """Returns `True` if `password` hashes to `hashed_password`."""
        return self.bcrypt.check_password_hash(hashed_password, password)

    def create_auth_tokens(self, user_id: int):
        access_token = create_access_token(
            user_id,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        refresh_token = create_refresh_token(
            user_id,
            expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
        )

        return access_token, refresh_token


security = Security()
