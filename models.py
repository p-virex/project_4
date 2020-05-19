from flask_security import UserMixin, RoleMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

user_orders = db.Table("user_orders", db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
                       db.Column("order_id", db.Integer, db.ForeignKey("orders.id")), )

food_categories = db.Table("food_categories", db.Column("food_id", db.Integer, db.ForeignKey("foods.id")),
                           db.Column("category_id", db.Integer, db.ForeignKey("categories.id")), )

orders_foods = db.Table("orders_foods", db.Column("order_id", db.Integer, db.ForeignKey("orders.id")),
                        db.Column("food_id", db.Integer, db.ForeignKey("foods.id")), )

roles_users = db.Table('roles_users', db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('roles.id')))


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    amount = db.Column(db.Integer)
    status = db.Column(db.String(100))
    mail = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    address = db.Column(db.String(255))
    users = db.relationship("User", secondary=user_orders, back_populates="orders")
    foods = db.relationship("Food", secondary=orders_foods, back_populates="orders")


class Food(db.Model):
    __tablename__ = "foods"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    price = db.Column(db.Integer)
    description = db.Column(db.String(255))
    picture = db.Column(db.String(100))
    categories = db.relationship("Category", secondary=food_categories, back_populates="foods")
    orders = db.relationship("Order", secondary=orders_foods, back_populates="foods")


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    foods = db.relationship("Food", secondary=food_categories, back_populates="categories")


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    orders = db.relationship("Order", secondary=user_orders, back_populates="users")
    roles = db.relationship('Role', secondary=roles_users, back_populates="users")


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))
    users = db.relationship('User', secondary=roles_users, back_populates="roles")
