from random import sample

from flask import render_template, request, redirect, session

from app import app, user_datastore
from common import get_login, get_cart, get_food_list, get_str_for_food, remove_error, get_date, get_sum_price, \
    check_password, hash_password
from form import LoginAuthForm, OrderedForm
from models import Category, User, Food, Order, db


@app.route('/')
def home_page():
    dict_food = dict()
    categories = db.session.query(Category).all()
    for category in categories:
        food_id = Category.query.filter(Category.id == category.id).scalar()
        dict_food.setdefault(category.title, sample(food_id.foods, 3))  # 3 - last three meals from list
    return render_template("main.html", dict_food=dict_food, login=get_login(), cart=get_cart())


@app.route('/cart/')
def cart_page():
    form = OrderedForm()
    error = ''
    if session.get('error'):
        error = session.get('error')
        remove_error()
    return render_template('cart.html', login=get_login(), error=error, cart=get_cart(), foods=get_food_list(),
                           count_foods=get_str_for_food(), total=get_sum_price(), form=form)


@app.route('/delete_food/<int:id_food>/')
def delete_food(id_food):
    foods_list_id = session.get('cart')
    if foods_list_id and id_food in foods_list_id:
        foods_list_id.remove(id_food)
        session['cart'] = foods_list_id
        food = db.session.query(Food).get(id_food)
        session['error'] = f'Блюдо: {food.title} удалено из корзины'
    return redirect('/cart/')


@app.route('/account/', methods=["GET", "POST"])
def account_page():
    form = LoginAuthForm()
    if request.method == 'POST':
        user_data = db.session.query(User).filter(User.email == form.login.data).first()
        if not user_data:
            session['error'] = 'Аккаунт не существует, Вы можете зарегистровать новый'
            return redirect('/register/')
        if all([form.login.data == user_data.email, check_password(user_data.password, form.password.data)]):
            session['id_user'] = user_data.id
            remove_error()
            return render_template('account.html', login=get_login(), orders=[])
        session['error'] = 'Неверный логин или пароль, поробуйте еще раз'
        return redirect('/user_login')
    if session.get('id_user'):
        orders = User.query.filter(User.id == session['id_user']).scalar()
        ordered_dict = {}
        for order in orders.orders:
            food_in_order = Order.query.filter(Order.id == order.id).scalar().foods
            ordered_dict[order] = food_in_order
        return render_template('account.html', login=get_login(), orders=ordered_dict)
    return redirect('/user_login')


@app.route('/register_db/', methods=["GET", "POST"])
def register():
    form = LoginAuthForm()
    if request.method == 'POST':
        user_data = db.session.query(User).get(form.login.data)
        if not user_data:
            user_datastore.create_user(name=form.name.data, email=form.login.data,
                                       password=hash_password(form.password.data))
            db.session.commit()
            return redirect('/account/')
    return redirect('/user_login/')


@app.route('/addtocart/<int:id_food>/')
def add_to_cart(id_food):
    if get_login():
        card = session.get('cart') if session.get('cart') else []
        if id_food not in card:
            card.append(id_food)
            session['cart'] = card
        else:
            session['error'] = 'Это блюдо уже есть в корзине!'
        return redirect('/cart/')
    session['error'] = 'Войдите на свой аккаунт или зарегистрируйтесь, чтобы добавлять товары в корзину'
    return redirect('/user_login')


@app.route('/user_login/')
def login_page():
    form = LoginAuthForm()
    error = session.get('error') if session.get('error') else ''
    remove_error()
    return render_template('login.html', form=form, error=error)


@app.route('/user_logout/')
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


@app.route('/ordered/', methods=["GET", "POST"])
def ordered_page():
    if not session.get('id_user'):
        return redirect('/user_login/')
    if request.method == 'POST':
        if not session.get('cart'):
            session['error'] = 'Вы не добавили хотя бы 1 блюдо'
            return redirect('/cart/')
        form = OrderedForm()
        user_data = db.session.query(User).get(session['id_user'])
        order = Order(address=form.address.data, phone=form.phone.data, date=get_date(), mail=user_data.email,
                      amount=form.amount.data, status='Обрабатывается')
        db.session.add(order)
        order.users.append(user_data)  # save user order
        for food_id in get_food_list():  # save in db list foods
            order.foods.append(food_id)
        db.session.commit()
        session.pop('cart')  # drop cart
        return render_template('ordered.html')
    if session.get('id_user'):
        return redirect('/account/')
    return redirect('/')
