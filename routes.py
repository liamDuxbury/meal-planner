"""Module for defining routes in the meal planner application."""
import random
from datetime import date, timedelta

from flask import jsonify, render_template

from app import app, db
from models.meal_planning import MealPlan, MealPlanRecipe, Recipe

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recipes', methods=['GET'])
def recipes():
    recipes = Recipe.query.all()
    if not recipes:
        recipes = []
        print("No recipes found in the database.")
    
    return render_template('recipes.html', recipes=recipes)


@app.route('/meal-plan', methods=['GET'])
def meal_plan():
    meal_plan = MealPlan.query.first()
    if not meal_plan:
        meal_plan = MealPlan()
        print("No meal plan found in the database.")
    
    return render_template('meal_plan.html', meal_plan=meal_plan)


@app.route('/meal-plan/generate', methods=['POST'])
def generate_meal_plan():
    # Get recipes
    recipes = Recipe.query.all()
    if len(recipes) < 7:
        return jsonify(error="Not enough recipes to generate a meal plan, run seed_recipes.sh"), 400
    # Select 7 random recipes
    selected = random.sample(recipes, 7)
    # Create a new meal plan with the selected recipes
    today = date.today()
    meal_plan = MealPlan(name=f"Meal plan {today.isoformat()}")
    meal_plan.recipes = [MealPlanRecipe(recipe_id=recipe.id, date=today + timedelta(days=i)) for i, recipe in enumerate(selected)]
    # Save the meal plan to the database
    db.session.add(meal_plan)
    db.session.commit()
    # Return the generated meal plan
    return jsonify(
        id=meal_plan.id,
        name=meal_plan.name,
        recipes=[
            {"date": mpr.date.isoformat(), "recipe_id": mpr.recipe_id}
            for mpr in meal_plan.recipes
        ],
    ), 201