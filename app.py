import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'instance', 'meal_planner.db')}"

db = SQLAlchemy()
migrate = Migrate()


def create_app(config=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    from routes import meal_plan_blueprint
    app.register_blueprint(meal_plan_blueprint)

    return app
