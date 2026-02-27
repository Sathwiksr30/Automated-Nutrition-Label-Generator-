import pandas as pd
import sqlite3
import os

print("Starting database creation...")

# Path to datasets folder
DATASET_PATH = "datasets"

# Create SQLite database
conn = sqlite3.connect("nutrition.db")

try:
    # Load CSV files with proper encoding
    recipes = pd.read_csv(
        os.path.join(DATASET_PATH, "Recipes.csv"),
        encoding="latin1"
    )

    snacks = pd.read_csv(
        os.path.join(DATASET_PATH, "Snacks.csv"),
        encoding="latin1"
    )

    ingredients = pd.read_csv(
        os.path.join(DATASET_PATH, "Ingredient.csv"),
        encoding="latin1"
    )

    print("CSV files loaded successfully ✅")

    # Clean column names
    recipes.columns = recipes.columns.str.strip().str.lower().str.replace(" ", "_")
    snacks.columns = snacks.columns.str.strip().str.lower().str.replace(" ", "_")
    ingredients.columns = ingredients.columns.str.strip().str.lower().str.replace(" ", "_")

    # Store data into SQLite tables
    recipes.to_sql("recipes", conn, if_exists="replace", index=False)
    snacks.to_sql("snacks", conn, if_exists="replace", index=False)
    ingredients.to_sql("ingredients", conn, if_exists="replace", index=False)

    print("Database created successfully ✅")

except Exception as e:
    print("Error occurred:", e)

finally:
    conn.close()
    print("Connection closed.")