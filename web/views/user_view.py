from flask import url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from werkzeug.utils import redirect
from wtforms import validators

from web import bcrypt


class UserView(ModelView):
    def is_accessible(self):
        if current_user.is_anonymous:
            return False
        return current_user.is_admin and current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.login'))

    column_display_pk = True
    column_labels = {
        'id': 'ID',
        'email': 'Емайл',
        'password': 'Пароль',
        'admin': 'Админ',
        'last_seen': 'Последний вход'
    }
    # Список отображаемых колонок
    column_list = ['id', 'admin', 'email', 'last_seen']

    column_sortable_list = ('id', 'admin', 'email')

    can_create = True
    can_edit = True
    can_delete = True
    can_export = False

    form_args = {
        'email': dict(label='Емайл', validators=[validators.Email()]),
        'password': dict(label='Пароль', validators=[validators.DataRequired()]),
    }

    column_searchable_list = ['email']
    column_editable_list = ['email', 'admin']

    create_modal = True
    edit_modal = True

    def on_model_change(self, form, model, is_created):
        model.password = bcrypt.generate_password_hash(model.password)
