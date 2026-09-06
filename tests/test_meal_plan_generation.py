from datetime import date, timedelta

import pytest
from sqlalchemy.exc import IntegrityError

from app import db
from models.meal_planning import Cuisine, MealPlan, MealPlanRecipe
from routes import generate_meal_plan_for_date, get_week_commencing_date

TARGET_DATE = date(2026, 1, 5)


def test_raises_when_fewer_than_seven_recipes(make_recipes):
    make_recipes(6, Cuisine.ITALIAN)

    with pytest.raises(ValueError, match='Not enough recipes'):
        generate_meal_plan_for_date(TARGET_DATE)


def test_fills_seven_consecutive_days_from_the_target_date(make_recipes):
    make_recipes(7, Cuisine.ITALIAN)

    meal_plan = generate_meal_plan_for_date(TARGET_DATE)

    assert len(meal_plan.recipes) == 7
    assert [r.date for r in meal_plan.recipes] == [
        TARGET_DATE + timedelta(days=i) for i in range(7)
    ]


def test_uses_each_recipe_at_most_once(make_recipes):
    make_recipes(7, Cuisine.ITALIAN)

    meal_plan = generate_meal_plan_for_date(TARGET_DATE)

    recipe_ids = [r.recipe_id for r in meal_plan.recipes]
    assert len(set(recipe_ids)) == 7


def test_cuisine_filter_only_selects_matching_recipes(make_recipes):
    make_recipes(7, Cuisine.THAI, prefix='Thai')
    make_recipes(7, Cuisine.FRENCH, prefix='French')

    meal_plan = generate_meal_plan_for_date(TARGET_DATE, [Cuisine.THAI.value])

    assert all(r.recipe.name.startswith('Thai') for r in meal_plan.recipes)


def test_cuisine_filter_that_matches_too_few_recipes_raises(make_recipes):
    make_recipes(7, Cuisine.THAI)
    make_recipes(3, Cuisine.FRENCH)

    with pytest.raises(ValueError, match='Not enough recipes'):
        generate_meal_plan_for_date(TARGET_DATE, [Cuisine.FRENCH.value])


def test_replacing_a_plan_leaves_exactly_one(make_recipes):
    make_recipes(7, Cuisine.ITALIAN)
    existing = generate_meal_plan_for_date(TARGET_DATE)

    generate_meal_plan_for_date(TARGET_DATE, replacing=existing)

    assert MealPlan.query.count() == 1


def test_a_recipe_cannot_appear_twice_in_the_same_plan(make_recipe):
    """The (meal_plan_id, recipe_id) composite key enforces this at schema level."""
    recipe = make_recipe('Pad Thai', Cuisine.THAI)
    meal_plan = MealPlan(name='Duplicate test')
    meal_plan.recipes = [
        MealPlanRecipe(recipe_id=recipe.id, date=TARGET_DATE),
        MealPlanRecipe(recipe_id=recipe.id, date=TARGET_DATE + timedelta(days=1)),
    ]
    db.session.add(meal_plan)

    with pytest.raises(IntegrityError):
        db.session.commit()


def test_week_commencing_is_always_the_next_monday():
    week_commencing = get_week_commencing_date()
    today = date.today()

    assert week_commencing.weekday() == 0
    assert today < week_commencing <= today + timedelta(days=7)
