import csv
import os

from app import app, db
from models import Category, Food


def filling_database():
    with app.app_context():
        csv_path = os.path.join(os.getcwd(), 'data', 'delivery_categories.csv')
        with open(csv_path, "r", encoding='utf-8') as f_obj:
            reader = csv.DictReader(f_obj, delimiter=',')
            for line in reader:
                db.session.add(Category(title=line["title"]))

        csv_path = os.path.join(os.getcwd(), 'data', 'delivery_items.csv')
        with open(csv_path, "r", encoding='utf-8') as f_obj:
            reader = csv.DictReader(f_obj, delimiter=',')
            for line in reader:
                food = Food(title=line["title"],
                            price=line["price"],
                            description=line["description"],
                            picture=line["picture"])
                db.session.add(food)
                id_food = db.session.query(Category).filter(Category.id == line["category_id"]).first()
                food.categories.append(id_food)
        db.session.commit()
