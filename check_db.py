import sqlite3

conn = sqlite3.connect("nutrition.db")
cursor = conn.cursor()

print("Searching for milk...")
cursor.execute("SELECT food_name FROM ingredients WHERE lower(food_name) LIKE '%milk%'")
print(cursor.fetchall())

cursor.execute("SELECT food FROM snacks WHERE lower(food) LIKE '%milk%'")
print(cursor.fetchall())

cursor.execute("SELECT dish_name FROM recipes WHERE lower(dish_name) LIKE '%milk%'")
print(cursor.fetchall())

print("\nSearching for tea...")
cursor.execute("SELECT food_name FROM ingredients WHERE lower(food_name) LIKE '%tea%'")
print(cursor.fetchall())

cursor.execute("SELECT food FROM snacks WHERE lower(food) LIKE '%tea%'")
print(cursor.fetchall())

cursor.execute("SELECT dish_name FROM recipes WHERE lower(dish_name) LIKE '%tea%'")
print(cursor.fetchall())

conn.close()