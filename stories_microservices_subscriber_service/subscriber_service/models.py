from sqlalchemy.sql import func
from .config.extensions import db


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


class Subscriber(SaveMixin, db.Model):
    email = db.Column(db.String(80), unique=True, nullable=False)

    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return self.email

    def __init__(self, email, is_active=True):
        self.email = email
        self.is_active = is_active