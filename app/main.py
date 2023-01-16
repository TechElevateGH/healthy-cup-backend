import os
from flask import Flask

from app.ents.employee import db, employees_blueprint

app = Flask(__name__, instance_relative_config=True)


def init_db():

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="sqlite:///roselle.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        DATABASE=os.path.join(app.instance_path, "roselle.sqlite"),
        SQLALCHEMY_ECHO=True,
    )

    db.init_app(app)

    with app.app_context():
        db.create_all()


def register_blueprints():
    app.register_blueprint(employees_blueprint)


if __name__ == "__main__":
    init_db()
    register_blueprints()
    app.run(debug=True)
