class AppConfig:
    DEBUG = True
    SECRET_KEY = "randomstring"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/project_database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
