from flask import render_template

from app import app


@app.route('/')
def home_page():
    return render_template('main.html')


@app.route('/cart/')
def cart_page():
    return render_template('cart.html')


@app.route('/account/')
def account_page():
    return render_template('account.html')


@app.route('/login/')
def login_page():
    return render_template('login.html')


@app.route('/logout/')
def logout_page():
    return render_template('logout.html')


@app.route('/register/')
def register_page():
    return render_template('register.html')


@app.route('/ordered/')
def ordered_page():
    return render_template('ordered.html')
