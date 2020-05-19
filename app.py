import csv
import os

from flask import Flask
from flask_migrate import Migrate
from configs import AppConfig
from models import db

app = Flask(__name__)
app.config.from_object(AppConfig)
db.init_app(app)

migrate = Migrate(app, db)

from views import *
from admin.admin import *


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
                food = Food(title=line["title"], price=line["price"], description=line["description"],
                            picture=line["picture"])
                db.session.add(food)
                id_food = db.session.query(Category).filter(Category.id == line["category_id"]).first()
                food.categories.append(id_food)
        db.session.commit()


def create_admin():
    with app.app_context():
        user_datastore.create_user(name='admin', email='admin', password='admin')
        user_datastore.create_role(name='admin', description='administrator')
        user = User.query.first()
        role = Role.query.first()
        user_datastore.add_role_to_user(user, role)
        db.session.commit()


if __name__ == '__main__':
    app.run(port=8060)
