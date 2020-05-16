from flask import render_template, request, redirect, session

from app import app
from form import LoginAuthForm
from models import Category, User, Food, db


def get_login():
    return True if session.get('id_user') else False


def remove_error():
    if session.get('error'):
        session.pop('error')


def get_price(id_food):
    food = db.session.query(Food).get(id_food)
    return int(food.price)


@app.route('/')
def home_page():
    dict_food = {}
    categories = db.session.query(Category).all()
    for category in categories:
        food_id = Category.query.filter(Category.id == category.id).scalar()
        dict_food.setdefault(category.title, food_id.foods[:3])
    cart = '' if not session.get('cart') else session.get('cart')  # todo
    print(sum(map(get_price, cart)))
    return render_template("main.html", dict_food=dict_food, login=get_login(), cart=cart)


@app.route('/cart/')
def cart_page():
    return render_template('cart.html', login=get_login())


@app.route('/account/', methods=["GET", "POST"])
def account_page():
    form = LoginAuthForm()
    if request.method == 'POST':
        user_data = db.session.query(User).filter(User.mail == form.login.data).first()
        if not user_data:
            session['error'] = 'Аккаунт не существует, Вы можете зарегистровать новый'
            return redirect('/register/')
        if all([form.login.data == user_data.mail, form.password.data == user_data.password]):
            session['id_user'] = user_data.id
            remove_error()
            return render_template('account.html', login=get_login())
    session['error'] = 'Неверный логин или пароль, поробуйте еще раз'
    return redirect('/login/')


@app.route('/register_db/', methods=["GET", "POST"])
def register():
    form = LoginAuthForm()
    if request.method == 'POST':
        user_data = db.session.query(User).get(form.login.data)
        if not user_data:
            # todo: add salt in the password
            db.session.add(User(mail=form.login.data, password=form.password.data))
            db.session.commit()
            return redirect('/account/')
    return redirect('/login/')


@app.route('/addtocart/<id_food>/')
def add_to_cart(id_food):
    session.setdefault('cart', []).append(int(id_food))
    print(id_food, session.get('cart'))
    return redirect('/cart/')


@app.route('/login/')
def login_page():
    form = LoginAuthForm()
    error = session.get('error') if session.get('error') else ''
    remove_error()
    return render_template('login.html', form=form, error=error)


@app.route('/logout/')
def logout_page():
    session.pop('id_user')
    if session.get('cart'):
        session.pop('cart')
    remove_error()
    return redirect('/')


@app.route('/register/')
def register_page():
    form = LoginAuthForm()
    error = session.get('error') if session.get('error') else ''
    remove_error()
    return render_template('register.html', form=form, error=error)


@app.route('/ordered/')
def ordered_page():
    return render_template('ordered.html')
