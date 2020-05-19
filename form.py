from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length


class LoginAuthForm(FlaskForm):
    login = StringField('mail', validators=[InputRequired(), Email()])
    name = StringField('name', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8)])


class OrderedForm(FlaskForm):
    address = StringField('address', validators=[InputRequired()])
    phone = StringField('phone', validators=[InputRequired()])
    amount = StringField('amount')
