from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List
import sqlite3
import os
import logging

from nutrition_engine import calculate_nutrition
from fssai_label import generate_fssai_label
from pdf_generator import generate_pdf

# ==========================
# APP INIT
# ==========================

app = FastAPI(title="Nutrition Label API", version="1.0")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "nutrition.db")

# ==========================
# LOGGING SETUP
# ==========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ==========================
# GLOBAL ERROR HANDLER
# ==========================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "data": None,
            "error": {
                "code": exc.status_code,
                "message": exc.detail
            }
        }
    )

# ==========================
# MODELS
# ==========================

class Ingredient(BaseModel):
    name: str = Field(..., min_length=1)
    weight: float = Field(..., gt=0)


class Recipe(BaseModel):
    serving_size: float = Field(..., ge=0)
    items: List[Ingredient]


# ==========================
# ROUTES
# ==========================

@app.get("/api/v1")
def home():
    return {
        "status": "success",
        "data": {
            "message": "Nutrition Label Generator API v1 running 🚀"
        },
        "error": None
    }


@app.get("/api/v1/search")
def search_food(q: str = Query(..., min_length=1)):

    logging.info(f"Search query received: {q}")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    results = []

    cursor.execute(
        "SELECT dish_name FROM recipes WHERE LOWER(dish_name) LIKE LOWER(?) LIMIT 5",
        (f"%{q}%",)
    )
    results += [row[0] for row in cursor.fetchall()]

    cursor.execute(
        "SELECT food FROM snacks WHERE LOWER(food) LIKE LOWER(?) LIMIT 5",
        (f"%{q}%",)
    )
    results += [row[0] for row in cursor.fetchall()]

    cursor.execute(
        "SELECT food_name FROM ingredients WHERE LOWER(food_name) LIKE LOWER(?) LIMIT 5",
        (f"%{q}%",)
    )
    results += [row[0] for row in cursor.fetchall()]

    conn.close()

    unique_results = list(set(results))

    return {
        "status": "success",
        "data": {
            "query": q,
            "results": unique_results
        },
        "error": None
    }


@app.post("/api/v1/generate-label")
def generate_label(recipe: Recipe):

    logging.info("Generate label request received")

    if len(recipe.items) == 0:
        raise HTTPException(status_code=400, detail="No ingredients provided.")

    items_list = [item.dict() for item in recipe.items]

    raw_nutrition, not_found_items, total_weight = calculate_nutrition(items_list)

    if not raw_nutrition:
        raise HTTPException(status_code=400, detail="No valid ingredients found in database.")

    serving_size = recipe.serving_size if recipe.serving_size > 0 else total_weight

    label = generate_fssai_label(
        nutrition_data=raw_nutrition,
        serving_size=serving_size,
        total_weight=total_weight
    )

    filename = generate_pdf(label)

    logging.info("Label generated successfully")

    return {
        "status": "success",
        "data": {
            "ingredients": items_list,
            "nutrition": label,
            "pdf": filename,
            "not_found_items": not_found_items
        },
        "error": None
    }