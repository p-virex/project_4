from flask import Flask
from flask_migrate import Migrate
from configs import AppConfig
from models import db

app = Flask(__name__)
app.config.from_object(AppConfig)
db.init_app(app)

migrate = Migrate(app, db)

from views import *

if __name__ == '__main__':
    app.run(port=8060)
