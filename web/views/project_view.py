import os

from flask import url_for, Markup, redirect
from flask_admin.contrib.sqla import ModelView
from flask_admin import form
from flask_login import current_user
from wtforms import validators

file_path = os.path.abspath(os.path.dirname(__name__))


def name_gen_img(model, file_data):
    hash_name = f'{model.title}/{file_data.filename}'
    return hash_name


class ProjectView(ModelView):
    def is_accessible(self):
        if current_user.is_anonymous:
            return False
        return current_user.is_admin and current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.login'))

    column_display_pk = True
    column_labels = {
        'id': 'ID',
        'image': 'Изображение',
        'title': 'Название',
        'preview': 'Краткое описание',
        'date': 'Дата',
        'link': 'Ссылка',
        'last_ed': 'Дата последнего изменения'
    }
    # Список отображаемых колонок
    column_list = ['id', 'image', 'title', 'preview', 'date', 'link', 'last_ed']

    column_default_sort = ('title', True)
    column_sortable_list = ('id', 'title', 'date')

    can_create = True
    can_edit = True
    can_delete = True
    can_export = False

    form_args = {
        'title': dict(label='Название', validators=[validators.DataRequired()]),
        'preview': dict(label='Краткое описание', validators=[validators.DataRequired()]),
        'link': dict(label='Ссылка', validators=[validators.DataRequired()]),
    }

    column_searchable_list = ['title', 'preview']
    column_editable_list = ['title', 'preview', 'link', 'date']

    create_modal = True
    edit_modal = True

    def _list_thumbnail(self, context, model, name):
        if not model.image:
            return ''
        url = url_for('static', filename=os.path.join('storage/img/', model.image))
        if model.image.split('.')[-1] in ('jpg', 'jpeg', 'png', 'svg', 'gif'):
            return Markup(f'<img src="{url}" width="100">')

    column_formatters = {
        'image': _list_thumbnail
    }

    form_extra_fields = {
        # ImageUploadField - проверка изображений, создание эскизов, обновление и удаление изображений
        "image": form.ImageUploadField('',
                                       base_path=os.path.join(file_path, 'web/static/storage/img/'),
                                       url_relative_path='storage/img/',
                                       namegen=name_gen_img,
                                       max_size=(1200, 700, True),
                                       thumbnail_size=(100, 100, True))
    }

    def create_form(self, obj=None):
        return super(ProjectView, self).create_form(obj)

    def edit_form(self, obj=None):
        return super(ProjectView, self).edit_form(obj)
