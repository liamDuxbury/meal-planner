"""Module for defining routes in the meal planner application."""
import random
from datetime import datetime, timedelta

from flask import jsonify, render_template, request

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
    data = request.get_json()
    override_existing = data.get('overrideExisting', False) if data else False

    today = datetime.today().date()
    days_until_next_monday = 7 - today.weekday()
    week_commencing_date = today + timedelta(days=days_until_next_monday)

    existing_meal_plan = MealPlan.query.filter(MealPlan.name == f"Meal plan {week_commencing_date.isoformat()}").first()
    if existing_meal_plan:
        if not override_existing:
            return jsonify(error="Meal plan for today already exists."), 409
        db.session.delete(existing_meal_plan)

    meal_plan = generate_meal_plan_for_date(week_commencing_date)
    return render_template('_meal_plan.html', meal_plan=meal_plan)


def generate_meal_plan_for_date(target_date):
    recipes = Recipe.query.all()

    if len(recipes) < 7:
        raise ValueError("Not enough recipes to generate a meal plan.")

    selected = random.sample(recipes, 7)
    meal_plan = MealPlan(name=f"Meal plan {target_date.isoformat()}")
    meal_plan.recipes = [MealPlanRecipe(recipe_id=recipe.id, date=target_date + timedelta(days=i)) for i, recipe in enumerate(selected)]

    db.session.add(meal_plan)
    db.session.commit()

    return meal_plan
