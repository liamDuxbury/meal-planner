from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

DATABASE_URI = 'sqlite:///meal_planner.db'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db = SQLAlchemy(app)

migrate = Migrate(app, db)


from meal_planner import routes  # noqa: F401, E402

with app.app_context():
    db.create_all()

