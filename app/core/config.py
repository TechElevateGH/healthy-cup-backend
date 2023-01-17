from dotenv import dotenv_values, find_dotenv
import secrets


class Config:
    config = dotenv_values(find_dotenv())
    config["SECRET_KEY"] = secrets.token_urlsafe()


config = Config().config
