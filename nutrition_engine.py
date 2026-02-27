import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "nutrition.db")


def normalize_key(key):
    key = key.lower().strip()

    mapping = {
        "calories_(kcal)": "Energy_kcal",
        "calories": "Energy_kcal",
        "cal_per_100_ml_or_gms": "Energy_kcal",

        "carbohydrates_(g)": "Carbohydrates_g",
        "carbs": "Carbohydrates_g",

        "protein_(g)": "Protein_g",
        "protein": "Protein_g",

        "fats_(g)": "Fat_g",
        "fat": "Fat_g",

        "satfat": "Saturated_Fat_g",

        "free_sugar_(g)": "Sugar_g",

        "fibre_(g)": "Fiber_g",
        "fiber": "Fiber_g",

        "sodium_(mg)": "Sodium_mg",

        "calcium_(mg)": "Calcium_mg",
        "iron_(mg)": "Iron_mg",
        "vitamin_c_(mg)": "Vitamin_C_mg",
        "folate_(âµg)": "Folate_ug"
    }

    return mapping.get(key, key)


def calculate_nutrition(items):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    total_nutrition = {}
    not_found = []
    total_weight = 0

    for item in items:

        name = item["name"].strip()
        weight = item["weight"]
        total_weight += weight
        found = False

        # ==========================
        # 1️⃣ SEARCH IN RECIPES TABLE
        # ==========================
        cursor.execute(
            "SELECT * FROM recipes WHERE LOWER(dish_name) = LOWER(?)",
            (name,)
        )
        row = cursor.fetchone()

        if not row:
            cursor.execute(
                "SELECT * FROM recipes WHERE LOWER(dish_name) LIKE LOWER(?)",
                (f"%{name}%",)
            )
            row = cursor.fetchone()

        if row:
            found = True
            columns = [desc[0] for desc in cursor.description]
            data = dict(zip(columns, row))

            for key, value in data.items():
                if key == "dish_name":
                    continue
                try:
                    value = float(value)
                except:
                    continue

                standardized_key = normalize_key(key)
                scaled = (value * weight) / 100
                total_nutrition[standardized_key] = total_nutrition.get(standardized_key, 0) + scaled

        # ==========================
        # 2️⃣ SEARCH IN SNACKS TABLE
        # ==========================
        if not found:
            cursor.execute(
                "SELECT * FROM snacks WHERE LOWER(food) = LOWER(?)",
                (name,)
            )
            row = cursor.fetchone()

            if not row:
                cursor.execute(
                    "SELECT * FROM snacks WHERE LOWER(food) LIKE LOWER(?)",
                    (f"%{name}%",)
                )
                row = cursor.fetchone()

            if row:
                found = True
                columns = [desc[0] for desc in cursor.description]
                data = dict(zip(columns, row))

                for key, value in data.items():
                    if key in ["food", "measure"]:
                        continue
                    try:
                        value = float(value)
                    except:
                        continue

                    standardized_key = normalize_key(key)
                    scaled = (value * weight) / 100
                    total_nutrition[standardized_key] = total_nutrition.get(standardized_key, 0) + scaled

        # ==========================
        # 3️⃣ SEARCH IN INGREDIENTS TABLE
        # ==========================
        if not found:
            cursor.execute(
                "SELECT * FROM ingredients WHERE LOWER(food_name) = LOWER(?)",
                (name,)
            )
            row = cursor.fetchone()

            if not row:
                cursor.execute(
                    "SELECT * FROM ingredients WHERE LOWER(food_name) LIKE LOWER(?)",
                    (f"%{name}%",)
                )
                row = cursor.fetchone()

            if row:
                found = True
                columns = [desc[0] for desc in cursor.description]
                data = dict(zip(columns, row))

                for key, value in data.items():
                    if key == "food_name":
                        continue
                    try:
                        value = float(value)
                    except:
                        continue

                    standardized_key = normalize_key(key)
                    scaled = (value * weight) / 100
                    total_nutrition[standardized_key] = total_nutrition.get(standardized_key, 0) + scaled

        if not found:
            not_found.append(name)

    conn.close()

    return total_nutrition, not_found, total_weight