from ..config.extensions import ma

from flask_marshmallow.fields import AbsoluteURLFor
from marshmallow import validates, ValidationError, fields, validate

from ..models import Subscriber


class SubscriberSchema(ma.SQLAlchemyAutoSchema):
    email = fields.Email(required=True, unique=True, validate=[validate.Length(min=7), ])

    class Meta:
        model = Subscriber
        include_fk = True
        load_instance = True

    @validates('email')
    def validate_email(self, value):
        if Subscriber.query.filter_by(email=value).first():
            raise ValidationError("You are already subscribed!")
        return True
