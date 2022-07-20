from web import db, create_app, login_manager
from flask import url_for, redirect, request, render_template
from flask_admin import expose, AdminIndexView
from flask_login import current_user, login_user, logout_user
from models import Education, User, Award, Publication, Project


class AdminMainView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login'))
        return self.render('admin/index.html', legend='Войти')

    @expose('/login/', methods=('GET', 'POST'))
    def login(self):
        if current_user.is_authenticated:
            return redirect(url_for('.index'))

        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter((User.email == email) & User.admin).first()
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('.index'))
            return self.render('admin/login.html', legend='Войти', message="Отказано в доступе")
        return self.render('admin/login.html', legend='Войти')

    @expose('/singup/', methods=('GET', 'POST'))
    def singup(self):
        if current_user.is_authenticated:
            return redirect(url_for('.index'))

        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            password_again = request.form.get('password_again')
            if password != password_again:
                return self.render('admin/signup.html', legend='Регистрация', message='Пароли не совпадают')
            if User.query.filter(User.email == email).first():
                return self.render('admin/signup.html', legend='Регистрация', message='Такой пользователь существует')

            user = User(
                is_admin=False,
                email=email,
                password=password
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('.index'))

        return self.render('admin/signup.html', legend='Регистрация')

    @expose('/logout/')
    def logout(self):
        logout_user()
        return redirect('/', 302)


app = create_app()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def main():
    educations = Education.query.all()
    awards = Award.query.all()
    publications = Publication.query.order_by(Publication.date.desc()).limit(3)
    projects = Project.query.all()
    return render_template('index.html', educations=educations, awards=awards,
                           publications=publications, projects=projects)


@app.route('/all_proj')
def all_proj():
    projects = Project.query.all()
    return render_template('all_proj.html', projects=projects)


@app.route('/all_pub')
def all_pub():
    publications = Publication.query.all()
    return render_template('all_pub.html', publications=publications)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)
