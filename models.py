from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

user_orders = db.Table(
    "user_orders",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("order_id", db.Integer, db.ForeignKey("orders.id")),
)

food_categories = db.Table(
    "food_categories",
    db.Column("food_id", db.Integer, db.ForeignKey("foods.id")),
    db.Column("category_id", db.Integer, db.ForeignKey("categories.id")),
)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String)
    password = db.Column(db.String)
    orders = db.relationship("Order", secondary=user_orders, back_populates="users")


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    amount = db.Column(db.String)
    status = db.Column(db.String)
    mail = db.Column(db.String)
    phone = db.Column(db.String)
    address = db.Column(db.String)
    users = db.relationship("User", secondary=user_orders, back_populates="orders")


class Food(db.Model):
    __tablename__ = "foods"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    price = db.Column(db.String)
    description = db.Column(db.String)
    picture = db.Column(db.String)
    categories = db.relationship("Category", secondary=food_categories, back_populates="foods")


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    foods = db.relationship("Food", secondary=food_categories, back_populates="categories")



