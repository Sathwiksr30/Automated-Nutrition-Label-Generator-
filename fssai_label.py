def generate_fssai_label(nutrition_data, serving_size, total_weight):

    if serving_size <= 0:
        serving_size = total_weight

    factor_100g = 100 / total_weight
    factor_serving = serving_size / total_weight

    per_100g = {}
    per_serving = {}

    # ---- Calculate scaled values ----
    for key, value in nutrition_data.items():
        per_100g[key] = round(value * factor_100g, 2)
        per_serving[key] = round(value * factor_serving, 2)

    # ---- Standard RDA values (FSSAI reference approx adult diet 2000 kcal) ----
    RDA = {
        "Energy_kcal": 2000,
        "Protein_g": 50,
        "Fat_g": 70,
        "Carbohydrates_g": 300,
        "Sugar_g": 50,
        "Sodium_mg": 2000
    }

    percent_rda = {}

    for nutrient, rda_value in RDA.items():
        if nutrient in per_serving and per_serving[nutrient] > 0:
            percent = (per_serving[nutrient] / rda_value) * 100
            percent_rda[f"{nutrient}_%RDA"] = round(percent, 2)

    return {
        "NUTRITION_INFORMATION": {
            "Per_100g": per_100g,
            "Per_Serving": per_serving,
            "Percent_RDA_Per_Serving": percent_rda
        },
        "Serving_Size_g": serving_size,
        "Total_Product_Weight_g": total_weight,
        "Note": "Percent RDA values are based on a 2000 kcal adult diet."
    }