import pytest

from app import create_app, db
from models.meal_planning import Cuisine, Recipe, RecipeCuisine


@pytest.fixture
def app():
    """An app bound to a throwaway in-memory database, torn down per test."""
    app = create_app({
        'SQLALCHEMY_DATABASE_URI': 'sqlite://',
        'TESTING': True,
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def make_recipe(app):
    def _make_recipe(name, *cuisines):
        recipe = Recipe(name=name)
        recipe.cuisines = [RecipeCuisine(cuisine=cuisine) for cuisine in cuisines]
        db.session.add(recipe)
        db.session.commit()
        return recipe

    return _make_recipe


@pytest.fixture
def make_recipes(make_recipe):
    def _make_recipes(count, *cuisines, prefix='Recipe'):
        return [make_recipe(f'{prefix} {i}', *cuisines) for i in range(count)]

    return _make_recipes
