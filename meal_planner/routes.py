"""Module for defining routes in the meal planner application."""
from flask import render_template

from meal_planner.app import app


@app.route('/')
def index():
    return render_template('index.html')