"""Defines ORM models for the meal planning application."""
import enum

from app import db


class Cuisine(str, enum.Enum):
    ITALIAN = "italian"
    INDIAN = "indian"
    THAI = "thai"
    FRENCH = "french"
    JAPANESE = "japanese"
    CHINESE = "chinese"
    MEXICAN = "mexican"
    MIDDLE_EASTERN = "middle_eastern"
    GREEK = "greek"
    SPANISH = "spanish"
    KOREAN = "korean"
    VIETNAMESE = "vietnamese"
    BRITISH = "british"
    AMERICAN = "american"


class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cuisines = db.relationship('RecipeCuisine', backref='recipe', cascade='all, delete-orphan', lazy=True)


class RecipeCuisine(db.Model):
    __tablename__ = 'recipe_cuisines'
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
    cuisine = db.Column(db.Enum(Cuisine), primary_key=True)


class MealPlan(db.Model):
    __tablename__ = 'meal_plans'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    recipes = db.relationship(
        'MealPlanRecipe',
        backref='meal_plan',
        cascade='all, delete-orphan',
        lazy=True,
        order_by='MealPlanRecipe.date',
    )


class MealPlanRecipe(db.Model):
    __tablename__ = 'meal_plan_recipes'
    meal_plan_id = db.Column(db.Integer, db.ForeignKey('meal_plans.id'), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
    date = db.Column(db.Date, nullable=False)
    recipe = db.relationship('Recipe')
