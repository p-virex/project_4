from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length


class LoginAuthForm(FlaskForm):
    login = StringField('name', validators=[InputRequired(), Email()])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8)])
