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
SQL

COUNT=$(sqlite3 "$DB_PATH" 'SELECT COUNT(*) FROM recipes;')
echo "Seeded $COUNT recipes into $DB_PATH"
