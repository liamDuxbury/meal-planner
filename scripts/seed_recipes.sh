#!/usr/bin/env bash
# Seeds the recipes table with sample data for local development/testing.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DB_PATH="$PROJECT_ROOT/instance/meal_planner.db"

if [ ! -f "$DB_PATH" ]; then
  echo "Database not found at $DB_PATH" >&2
  echo "Run the Flask app once first (flask run) so it can create the database, then re-run this script." >&2
  exit 1
fi

sqlite3 "$DB_PATH" <<'SQL'
DELETE FROM recipe_cuisines;
DELETE FROM recipes;

INSERT INTO recipes (name) VALUES
  ('Spaghetti Carbonara'),
  ('Margherita Pizza'),
  ('Lasagna alla Bolognese'),
  ('Risotto ai Funghi'),
  ('Chicken Tikka Masala'),
  ('Lamb Rogan Josh'),
  ('Palak Paneer'),
  ('Chana Masala'),
  ('Butter Chicken'),
  ('Pad Thai'),
  ('Green Curry Chicken'),
  ('Tom Yum Soup'),
  ('Massaman Curry'),
  ('Beef Bourguignon'),
  ('Coq au Vin'),
  ('Ratatouille'),
  ('Quiche Lorraine'),
  ('Sushi Rolls'),
  ('Chicken Katsu Curry'),
  ('Tonkotsu Ramen'),
  ('Teriyaki Salmon'),
  ('Kung Pao Chicken'),
  ('Mapo Tofu'),
  ('Sweet and Sour Pork'),
  ('Dan Dan Noodles'),
  ('Beef Tacos'),
  ('Chicken Enchiladas'),
  ('Guacamole and Chips'),
  ('Pork Carnitas'),
  ('Falafel Wrap'),
  ('Chicken Shawarma'),
  ('Hummus with Pita'),
  ('Lamb Kofta'),
  ('Moussaka'),
  ('Greek Salad'),
  ('Souvlaki Skewers'),
  ('Spanakopita'),
  ('Paella Valenciana'),
  ('Patatas Bravas'),
  ('Gazpacho'),
  ('Tortilla Espanola'),
  ('Bibimbap'),
  ('Korean Fried Chicken'),
  ('Kimchi Jjigae'),
  ('Bulgogi'),
  ('Pho Bo'),
  ('Banh Mi Sandwich'),
  ('Fish and Chips'),
  ('Shepherds Pie'),
  ('Sunday Roast Chicken'),
  ('Bangers and Mash'),
  ('BBQ Pulled Pork'),
  ('Classic Cheeseburger'),
  ('Mac and Cheese'),
  ('Buffalo Chicken Wings');

INSERT INTO recipe_cuisines (recipe_id, cuisine)
SELECT r.id, m.cuisine
FROM recipes r
JOIN (
SELECT column1 AS name, column2 AS cuisine
FROM (VALUES
  ('Spaghetti Carbonara', 'ITALIAN'),
  ('Margherita Pizza', 'ITALIAN'),
  ('Lasagna alla Bolognese', 'ITALIAN'),
  ('Risotto ai Funghi', 'ITALIAN'),
  ('Chicken Tikka Masala', 'INDIAN'),
  ('Lamb Rogan Josh', 'INDIAN'),
  ('Palak Paneer', 'INDIAN'),
  ('Chana Masala', 'INDIAN'),
  ('Butter Chicken', 'INDIAN'),
  ('Pad Thai', 'THAI'),
  ('Green Curry Chicken', 'THAI'),
  ('Tom Yum Soup', 'THAI'),
  ('Massaman Curry', 'THAI'),
  ('Beef Bourguignon', 'FRENCH'),
  ('Coq au Vin', 'FRENCH'),
  ('Ratatouille', 'FRENCH'),
  ('Quiche Lorraine', 'FRENCH'),
  ('Sushi Rolls', 'JAPANESE'),
  ('Chicken Katsu Curry', 'JAPANESE'),
  ('Tonkotsu Ramen', 'JAPANESE'),
  ('Teriyaki Salmon', 'JAPANESE'),
  ('Kung Pao Chicken', 'CHINESE'),
  ('Mapo Tofu', 'CHINESE'),
  ('Sweet and Sour Pork', 'CHINESE'),
  ('Dan Dan Noodles', 'CHINESE'),
  ('Beef Tacos', 'MEXICAN'),
  ('Chicken Enchiladas', 'MEXICAN'),
  ('Guacamole and Chips', 'MEXICAN'),
  ('Pork Carnitas', 'MEXICAN'),
  ('Falafel Wrap', 'MIDDLE_EASTERN'),
  ('Chicken Shawarma', 'MIDDLE_EASTERN'),
  ('Hummus with Pita', 'MIDDLE_EASTERN'),
  ('Lamb Kofta', 'MIDDLE_EASTERN'),
  ('Moussaka', 'GREEK'),
  ('Greek Salad', 'GREEK'),
  ('Souvlaki Skewers', 'GREEK'),
  ('Spanakopita', 'GREEK'),
  ('Paella Valenciana', 'SPANISH'),
  ('Patatas Bravas', 'SPANISH'),
  ('Gazpacho', 'SPANISH'),
  ('Tortilla Espanola', 'SPANISH'),
  ('Bibimbap', 'KOREAN'),
  ('Korean Fried Chicken', 'KOREAN'),
  ('Kimchi Jjigae', 'KOREAN'),
  ('Bulgogi', 'KOREAN'),
  ('Pho Bo', 'VIETNAMESE'),
  ('Banh Mi Sandwich', 'VIETNAMESE'),
  ('Fish and Chips', 'BRITISH'),
  ('Shepherds Pie', 'BRITISH'),
  ('Sunday Roast Chicken', 'BRITISH'),
  ('Bangers and Mash', 'BRITISH'),
  ('BBQ Pulled Pork', 'AMERICAN'),
  ('Classic Cheeseburger', 'AMERICAN'),
  ('Mac and Cheese', 'AMERICAN'),
  ('Buffalo Chicken Wings', 'AMERICAN')
)
) AS m
ON r.name = m.name;
SQL

RECIPE_COUNT=$(sqlite3 "$DB_PATH" 'SELECT COUNT(*) FROM recipes;')
CUISINE_COUNT=$(sqlite3 "$DB_PATH" 'SELECT COUNT(*) FROM recipe_cuisines;')
echo "Seeded $RECIPE_COUNT recipes and $CUISINE_COUNT recipe-cuisine links into $DB_PATH"
