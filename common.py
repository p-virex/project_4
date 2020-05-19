import hashlib
import uuid
from datetime import datetime

from flask import session

from models import db, User, Food


def check_password(hashed_password, user_password):
    """
    Function for checking the correct password
    :param hashed_password: hashed password from db
    :param user_password: input user password
    :return: bool, true if password correct
    """
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()


def hash_password(password):
    """
    Function for hashing password
    :param password: user password
    :return: hashing user password + random salt
    """
    salt = uuid.uuid4().hex  # generate salt
    # example: www == 	6e3204b0f821234d4591b77d52c35540113fd31f818d1fbb1e63a701685d490e:6e463646a7654778aa9488d905f41482
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def get_login():
    """
    Get login status for current session.
    :return: bool, true if user login
    """
    return True if session.get('id_user') else False


def remove_error():
    """
    Remove errors if they is.
    """
    if session.get('error'):
        session.pop('error')


def get_price(id_food):
    """
    Get price meal from database.
    :param id_food: id food in database
    :return: food price from database
    """
    food = db.session.query(Food).get(id_food)
    return int(food.price)


def get_sum_price():
    """
    Get total sum meals from cart
    :return: total sum meals from cart
    """
    cart = '' if not session.get('cart') else session.get('cart')
    return sum(map(get_price, cart))


def get_cart():
    """
    Get str for head cart
    """
    return f'Здравствуйте, {get_user_name()}! Стоимость Вашего заказа: {get_sum_price()}' if get_login() else ''


def get_user_name():
    if session.get('id_user'):
        user = db.session.query(User).get(session.get('id_user'))
        return user.name


def get_food_list():
    return [] if not session.get('cart') else [db.session.query(Food).get(id_food) for id_food in session['cart']]


def get_date():
    now_date = datetime.now()
    return now_date.strftime("%A, %d. %B %Y %I:%M%p")


def get_str_for_food():
    l_f = str(len(get_food_list()))
    if l_f.endswith('1'):
        return 'Блюдо'
    elif any([l_f.endswith('2'), l_f.endswith('3'), l_f.endswith('4')]):
        return 'Блюда'
    else:
        return 'Блюд'
