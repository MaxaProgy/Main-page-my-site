from flask import url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from werkzeug.utils import redirect
from wtforms import validators


class AwView(ModelView):
    def is_accessible(self):
        if current_user.is_anonymous:
            return False
        return current_user.is_admin and current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.login'))

    column_display_pk = True
    column_labels = {
        'id': 'ID',
        'title': 'Название',
        'period': 'Дата получения',
        'link': 'Ссылка',
        'date': 'Дата публикации',
        'last_ed': 'Дата последнего редактирования'
    }
    # Список отображаемых колонок
    column_list = ['id', 'title', 'period', 'link', 'date', 'last_ed']

    column_default_sort = ('title', True)
    column_sortable_list = ('id', 'title', 'period', 'link', 'date')

    can_create = True
    can_edit = True
    can_delete = True
    can_export = False

    form_args = {
        'title': dict(label='Название', validators=[validators.DataRequired()]),
        'period': dict(label='Дата получения', validators=[validators.DataRequired()]),
        'link': dict(label='Ссылка', validators=[validators.DataRequired()]),
    }

    column_searchable_list = ['title', 'period']
    column_editable_list = ['title', 'period', 'link', 'date']

    create_modal = True
    edit_modal = True
