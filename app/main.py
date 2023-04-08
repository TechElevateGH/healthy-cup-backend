from flask import Flask
from flask_jwt_extended import JWTManager

from app.core.security import security
from app.core.settings import settings
from app.ents.base.crud import db, migrate
from app.ents.employee import employee_blueprint


def init_db(app: Flask) -> None:
    """Initialize SQLite database and create tables for `app`."""
    print(settings.SQLALCHEMY_DATABASE_URI)
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.SQLALCHEMY_DATABASE_URI

    db.init_app(app)

    # *  Will later create tables with Alembic
    with app.app_context():
        db.create_all()


def register_blueprints(app: Flask) -> None:
    """Register `app` blueprints."""
    app.register_blueprint(employee_blueprint)

def configure_jwt(app: Flask) -> None:
    app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET_KEY
    JWTManager(app)


def create_app() -> Flask:
    app = Flask(__name__)
    security.bcrypt.init_app(app)
    init_db(app)
    register_blueprints(app)
    configure_jwt(app)
    migrate.init_app(app, db)
    return app


app = create_app()
