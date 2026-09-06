"""Module for defining routes in the meal planner application."""
from flask import render_template

from app import app
from models.meal_planning import Recipe


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recipes', methods=['GET'])
def recipes():
    recipes = Recipe.query.all()
    if not recipes:
        recipes = []
    
    return render_template('recipes.html', recipes=recipes)
