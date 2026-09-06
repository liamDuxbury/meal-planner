import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Avoid using relative paths, causes issues when running migrations
basedir = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.dirname(basedir)
DATABASE_URI = f"sqlite:///{os.path.join(project_root, 'instance', 'meal_planner.db')}"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db = SQLAlchemy(app)

import routes  # noqa: F401, E402
