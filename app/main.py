import os

from flask import Flask

from app.core.config import settings
from app.core.security import security
from app.ents.base.crud import db
from app.ents.employee import employee_blueprint


def init_db(app: Flask) -> None:
    """Initialize SQLite database and create tables for `app`."""
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, "healthycup.sqlite"),
        SQLALCHEMY_DATABASE_URI=settings.SQLALCHEMY_DATABASE_URI,
        # SQLALCHEMY_TRACK_MODIFICATIONS=settings.SQLALCHEMY_TRACK_MODIFICATIONS,
        # SQLALCHEMY_ECHO=settings.get("SQLALCHEMY_ECHO"),
    )

    db.init_app(app)

    # *  Will later create tables with Alembic
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
