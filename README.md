# Meal Planner

A meal planning application with user authentication, recipe selection, and dietary requirement management.

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

