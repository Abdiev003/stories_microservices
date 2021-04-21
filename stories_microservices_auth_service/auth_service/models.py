from flask import url_for, render_template
from sqlalchemy.sql import func
from flask_login import UserMixin

from .config.extensions import db, login_manager
from werkzeug.security import generate_password_hash

from .publisher import Publish
from .utils.tokens import generate_confirmation_token


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


class SaveMixin(object):
    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(),
                           server_onupdate=func.now(), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class User(UserMixin, SaveMixin, db.Model):
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(150), nullable=True)
    email = db.Column(db.String(254), nullable=False)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    date_joined = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    bio = db.Column(db.TEXT, nullable=True)
    image = db.Column(db.String(500), nullable=True)
    is_superuser = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, username, password, first_name=None, last_name=None, bio=None,
                 image=None, is_active=False, date_joined=None, is_superuser=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)
        self.is_active = is_active
        self.bio = bio
        self.image = image
        self.date_joined = date_joined
        self.is_superuser = is_superuser

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


    def send_confirmation_mail(self):
        token = generate_confirmation_token(self.email)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('user/activate.html', confirm_url=confirm_url, user=self)
        subject = 'Confirm your account'
        to = (self.email,)
        data = {
            'subject': subject,
            'body': html,
            'to': to
        }
        Publish(data=data, event_type='send_mail')