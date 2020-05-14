import os

import csv

from flask import Flask
from flask_migrate import Migrate
from configs import AppConfig
from models import db, Category

app = Flask(__name__)
app.config.from_object(AppConfig)
db.init_app(app)

migrate = Migrate(app, db)

from views import *

with app.app_context():
    db.create_all()


def csv_reader(file_obj):
    """
    Read a csv file
    """
    reader = csv.DictReader(file_obj, delimiter=',')
    for line in reader:
        print(line)
        db.session.add(Category(title=line["title"]))
    db.session.commit()


def filling_database():
    csv_path = os.path.join(os.getcwd(), 'data', 'delivery_categories.csv')
    with open(csv_path, "r") as f_obj:
        csv_reader(f_obj)


if __name__ == '__main__':
    csv_path = os.path.join(os.getcwd(), 'data', 'delivery_categories.csv')
    with open(csv_path, "r") as f_obj:
        csv_reader(f_obj)
    # app.run(port=8060)
