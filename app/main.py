import os

from flask import Flask

from app.core.config import config
from app.core.security import security
from app.ents.base.crud import db
from app.ents.employee import employee_blueprint


def init_db(app: Flask) -> None:
    """Initialize SQLite database and create tables for `app`."""
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, "healthycup.sqlite"),
        SQLALCHEMY_DATABASE_URI=config.get("SQLALCHEMY_DATABASE_URI"),
        SQLALCHEMY_TRACK_MODIFICATIONS=config.get("SQLALCHEMY_TRACK_MODIFICATIONS"),
        SQLALCHEMY_ECHO=config.get("SQLALCHEMY_ECHO"),
    )

    db.init_app(app)

    with app.app_context():
        db.create_all()


def register_blueprints(app: Flask) -> None:
    """Register `app` blueprints."""
    app.register_blueprint(employee_blueprint)


def create_app() -> Flask:
    app = Flask(__name__)
    security.bcrypt.init_app(app)
    init_db(app)
    register_blueprints(app)
    return app


app = create_app()
