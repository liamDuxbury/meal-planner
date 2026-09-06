"""Module for defining routes in the meal planner application."""
import random
from datetime import datetime, timedelta

from flask import render_template, request

from app import app, db
from models.meal_planning import MealPlan, MealPlanRecipe, Recipe, Cuisine, RecipeCuisine


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
    week_commencing_date = get_week_commencing_date()
    meal_plan = get_meal_plan_for_date(week_commencing_date)
    if not meal_plan:
        meal_plan = MealPlan()
        print("No meal plan found in the database.")

    return render_template('meal_plan.html', meal_plan=meal_plan, cuisines=Cuisine)


@app.route('/meal-plan/generate', methods=['POST'])
def generate_meal_plan():
    data = request.get_json()
    override_existing = data.get('overrideExisting', False) if data else False
    cuisine_filters = (data.get('cuisines') or []) if data else []

    week_commencing_date = get_week_commencing_date()
    existing_meal_plan = get_meal_plan_for_date(week_commencing_date)

    if existing_meal_plan and not override_existing:
        return render_template(
            '_meal_plan.html',
            meal_plan=existing_meal_plan,
            notice='A plan for this week already exists. Tick "Override existing meal plan" to regenerate it.',
        )

    try:
        meal_plan = generate_meal_plan_for_date(week_commencing_date, cuisine_filters, existing_meal_plan)
    except ValueError as e:
        return render_template('_meal_plan.html', meal_plan=existing_meal_plan, error=str(e)), 400

    return render_template('_meal_plan.html', meal_plan=meal_plan)


def generate_meal_plan_for_date(target_date, cuisine_filters=None, replacing=None):
    query = Recipe.query
    if cuisine_filters:
        cuisine_enums = [Cuisine(value) for value in cuisine_filters]
        query = query.join(RecipeCuisine).filter(RecipeCuisine.cuisine.in_(cuisine_enums)).distinct()

    recipes = query.all()

    if len(recipes) < 7:
        raise ValueError("Not enough recipes to fill a week. Try selecting more cuisines.")

    if replacing:
        db.session.delete(replacing)

    selected = random.sample(recipes, 7)
    meal_plan = MealPlan(name=f"Meal plan {target_date.isoformat()}")
    meal_plan.recipes = [MealPlanRecipe(recipe_id=recipe.id, date=target_date + timedelta(days=i)) for i, recipe in enumerate(selected)]

    db.session.add(meal_plan)
    db.session.commit()

    return meal_plan


def get_week_commencing_date():
    today = datetime.today().date()
    days_until_next_monday = 7 - today.weekday()
    return today + timedelta(days=days_until_next_monday)


def get_meal_plan_for_date(target_date):
    meal_plan = MealPlan.query.filter(MealPlan.name == f"Meal plan {target_date.isoformat()}").first()
    return meal_plan