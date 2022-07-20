from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)
    from run import AdminMainView
    from models import User, Education, Award, Publication, Project
    from web.views import UserView, EdView, AwView, PubView, ProjectView

    admin = Admin(app, 'M@X@', index_view=AdminMainView(), template_mode='bootstrap4', url='/')

    admin.add_view(UserView(User, db.session, category='Админка',
                            name='Пользователи', endpoint='admin/user'))
    admin.add_view(EdView(Education, db.session, category='Админка',
                          name='Образование', endpoint='admin/ed'))
    admin.add_view(AwView(Award, db.session, category='Админка',
                          name='Достижения', endpoint='admin/aw'))
    admin.add_view(ProjectView(Project, db.session, category='Админка',
                               name='Проекты', endpoint='admin/project'))
    admin.add_view(PubView(Publication, db.session, category='Админка',
                           name='Публикации', endpoint='admin/pub'))

    return app
