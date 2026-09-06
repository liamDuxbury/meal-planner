from models.meal_planning import Cuisine, MealPlan
from routes import generate_meal_plan_for_date, get_week_commencing_date


def plan_for_this_week():
    return generate_meal_plan_for_date(get_week_commencing_date())


def test_recipes_page_lists_recipe_names(client, make_recipe):
    make_recipe('Pad Thai', Cuisine.THAI)

    response = client.get('/recipes')

    assert response.status_code == 200
    assert b'Pad Thai' in response.data


def test_meal_plan_page_shows_empty_state_when_no_plan_exists(client):
    response = client.get('/meal-plan')

    assert response.status_code == 200
    assert b'No meal plan generated yet.' in response.data


def test_generate_creates_a_plan_for_the_coming_week(client, make_recipes):
    make_recipes(7, Cuisine.ITALIAN)

    response = client.post('/meal-plan/generate', json={})

    assert response.status_code == 200
    assert MealPlan.query.count() == 1
    assert b'Recipe 0' in response.data


def test_generate_refuses_to_overwrite_an_existing_plan(client, make_recipes):
    make_recipes(7, Cuisine.ITALIAN)
    existing_recipe_ids = [r.recipe_id for r in plan_for_this_week().recipes]

    response = client.post('/meal-plan/generate', json={'overrideExisting': False})

    assert b'already exists' in response.data
    assert [r.recipe_id for r in MealPlan.query.one().recipes] == existing_recipe_ids


def test_generate_replaces_the_plan_when_override_is_set(client, make_recipes):
    make_recipes(7, Cuisine.ITALIAN)
    original_id = plan_for_this_week().id

    response = client.post('/meal-plan/generate', json={'overrideExisting': True})

    assert response.status_code == 200
    assert MealPlan.query.count() == 1
    assert MealPlan.query.one().id != original_id


def test_generate_returns_400_when_there_are_too_few_recipes(client, make_recipes):
    make_recipes(3, Cuisine.ITALIAN)

    response = client.post('/meal-plan/generate', json={})

    assert response.status_code == 400
    assert b'Not enough recipes' in response.data
    assert MealPlan.query.count() == 0
