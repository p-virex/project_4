from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from app import app
from models import db, User, Order, Category, Food, Role
from flask_security import SQLAlchemyUserDatastore, Security, current_user
from flask import redirect, url_for, request


class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class AdminView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


admin = Admin(app, 'Flask', url='/', index_view=HomeAdminView(name='Home'))

admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Order, db.session))
admin.add_view(AdminView(Category, db.session))
admin.add_view(AdminView(Food, db.session))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
