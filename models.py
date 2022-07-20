from web import bcrypt

from web import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tabelname__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, email, is_admin, password):
        self.email = email
        self.set_password(password)
        self.admin = is_admin

    def __repr__(self):
        return '<User %r>' % self.id

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_anonymous(self):
        return False

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Project(db.Model):
    __tabelname__ = 'project'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    image = db.Column(db.String, nullable=False, default='default.jpg')

    title = db.Column(db.String, nullable=False)
    preview = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Project %r>' % self.id


class Publication(db.Model):
    __tabelname__ = 'publication'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    link = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Publication %r>' % self.id


class Education(db.Model):
    __tabelname__ = 'education'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String, nullable=False)
    period = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Education %r>' % self.id


class Award(db.Model):
    __tabelname__ = 'award'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String, nullable=False)
    period = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Award %r>' % self.id
