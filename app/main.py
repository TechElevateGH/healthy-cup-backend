from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from app.core.security import security
from app.core.settings import settings
from app.ents.admin import admin_blueprint
from app.ents.base import base_endpoints
from app.ents.base.crud import db
from app.ents.employee import employee_blueprint

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

migrate = Migrate()


def init_db(app: Flask) -> None:
    """Initialize database and create tables for `app`."""

    # *  Create tables with Alembic
    with app.app_context():
        db.create_all()


def register_blueprints(app: Flask) -> None:
    """Register `app` blueprints."""
    app.register_blueprint(employee_blueprint)
    app.register_blueprint(base_endpoints)
    app.register_blueprint(admin_blueprint)

sentry_sdk.init(
    dsn = settings.SENTRY_DSN,
    integrations=[
        FlaskIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(settings)

    JWTManager(app)
    db.init_app(app)
    security.bcrypt.init_app(app)
    migrate.init_app(app, db)

    #! Needs to be removed. Prefer migration with Alembic
    init_db(app)

    register_blueprints(app)
    return app


app = create_app()
