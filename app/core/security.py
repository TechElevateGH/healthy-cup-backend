from flask_bcrypt import Bcrypt


class Security:
    bcrypt = Bcrypt()

    def hash_password(self, password: str) -> str:
        return self.bcrypt.generate_password_hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.bcrypt.check_password_hash(password, hashed_password)


security = Security()
