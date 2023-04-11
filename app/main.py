from flask import Flask
from flask_jwt_extended import JWTManager

from app.core.security import security
from app.core.settings import settings
from app.ents.base import base_endpoints
from app.ents.base.crud import db
from app.ents.employee import employee_blueprint

from flask_migrate import Migrate

migrate = Migrate()


def init_db(app: Flask) -> None:
    """Initialize database and create tables for `app`."""

    # *  Create tables with Alembic
    # with app.app_context():
    #     db.create_all()
    ...


def register_blueprints(app: Flask) -> None:
    """Register `app` blueprints."""
    app.register_blueprint(employee_blueprint)
    app.register_blueprint(base_endpoints)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(settings)

    JWTManager(app)
    db.init_app(app)
    security.bcrypt.init_app(app)
    migrate.init_app(app, db)

    register_blueprints(app)
    return app


app = create_app()
