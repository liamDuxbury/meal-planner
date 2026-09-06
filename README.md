# Meal Planner

A meal planning application with user authentication, recipe selection, and dietary requirement management.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask run
```

To run with hotreloading, run:
```bash
flask  --debug run 
```

The app creates its SQLite database automatically on first run, at `instance/meal_planner.db`.

To populate the recipes table with sample data:

```bash
./scripts/seed_recipes.sh
```

## Migrations

Schema changes are managed with Flask-Migrate (Alembic), run from the `meal_planner/` directory:

```bash
flask db migrate -m "describe the change"   # autogenerate a revision from model changes
flask db upgrade                            # apply pending migrations
```

Always review the generated file under `migrations/versions/` before running `upgrade`.

To query the SQLite instance directy:
```bash
sqlite3 instance/meal_planner.db "SELECT * FROM recipe_cuisines;"
```

## Technology Stack

| Layer | Technology |
|-------|------------|
| **Framework** | Flask (Python) |
| **Frontend** | Jinja2 templating |
| **Database** | SQLite |
| **ORM** | SQLAlchemy |


## Data Model

### Recipe
| Field | Type | Notes |
|-------|------|-------|
| `id` | Integer | Primary key |
| `name` | String | Recipe title |
| `cuisines` | Array/String | Tags (Italian, Asian, etc.) |
| `dietary_requirements` | Array/String | Vegan, vegetarian, gluten-free, etc. |
| `ingredient_list` | Text/JSON | List of ingredients with quantities |

### User
| Field | Type | Notes |
|-------|------|-------|
| `id` | Integer | Primary key |
| `name` | String | User's display name |
| `password` | String | Encrypted password (bcrypt or similar) |
| `is_super_admin` | Boolean | Admin privileges flag |
| `dietary_requirements` | Array/String | User's dietary restrictions |

### Meal Plan
| Field        | Type     | Notes                              |
| ------------ | -------- | ---------------------------------- |
| `id`         | Integer  | Primary key                        |
| `name`       | String   | Plan name (e.g., "Week of Sept 5") |
| `plan_id`    | Integer  | FK to Plan                         |
| `owner_id`   | Integer  | FK to User                         |
| `created_at` | DateTime | Timestamp                          |
### Plan
| Field        | Type     | Notes        |
| ------------ | -------- | ------------ |
| `id`         | Integer  | Primary key  |
| `recipe_id`  | Integer  | FK to Recipe |
| `date`       | DateTime | Timestampt   |
| `owner_id`   | Integer  | FK to User   |
| `created_at` | DateTime | Timestamp    |

