class AppConfig:
    DEBUG = True
    SECRET_KEY = "randomstring"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/project_database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = 'A80hvh7GTdckkhB1Blbacb67Sdlkbc!bnls3ac#@'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
