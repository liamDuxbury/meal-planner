"""Module for defining routes in the meal planner application."""
import random
from datetime import date, timedelta

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
    # Get recipes
    data = request.get_json()
    override_existing = data.get('overrideExisting', False) if data else False
    print(f"Override existing meal plan: {override_existing}")
    print(f"Request data: {data}")
    recipes = Recipe.query.all()
    if len(recipes) < 7:
        return jsonify(error="Not enough recipes to generate a meal plan, run seed_recipes.sh"), 400
    # Select 7 random recipes
    selected = random.sample(recipes, 7)
    # Create a new meal plan with the selected recipes
    today = date.today()
    existing_meal_plan = MealPlan.query.filter(MealPlan.name == f"Meal plan {today.isoformat()}").first()
    if existing_meal_plan:
        if not override_existing:
            return jsonify(error="Meal plan for today already exists."), 409
        db.session.delete(existing_meal_plan)
    meal_plan = MealPlan(name=f"Meal plan {today.isoformat()}")
    meal_plan.recipes = [MealPlanRecipe(recipe_id=recipe.id, date=today + timedelta(days=i)) for i, recipe in enumerate(selected)]
    # Save the meal plan to the database
    db.session.add(meal_plan)
    db.session.commit()
    # Return the generated meal plan
    return render_template('_meal_plan.html', meal_plan=meal_plan)
