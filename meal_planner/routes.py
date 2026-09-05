"""Module for defining routes in the meal planner application."""
from flask import app, render_template


@app.route('/')
def index():
    return render_template('template/index.html')