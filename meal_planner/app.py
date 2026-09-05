from flask import Flask
from flask_sqlalchemy import SQLAlchemy

DATABASE_URI = 'sqlite:///meal_planner.db'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db = SQLAlchemy(app)

from meal_planner import routes  # noqa: E402x

with app.app_context():
    db.create_all()

