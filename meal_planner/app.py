from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database import get_db, close_connection, DATABASE_URI

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db = SQLAlchemy(app)
db.create_all()
