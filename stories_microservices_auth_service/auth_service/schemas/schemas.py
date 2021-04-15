from ..config.extensions import ma

from flask_marshmallow.fields import AbsoluteURLFor
from marshmallow import validate, ValidationError, fields, validates

from ..models import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    image = AbsoluteURLFor(
        'uploaded_file',
        filename='<image>'
    )

    password = ma.String(load_only=True, required=True, validate=[validate.Length(min=8, max=32)])
    email = fields.Email(required=True, unique=True, validate=[validate.Length(min=7)])

    class Meta:
        model = User
        include_fk = True
        load_instance = True
        exclude = (
            'is_superuser',
            'is_active'
        )

    @validates('email')
    def validate_email(self, email):
        if User.query.filter_by(email=email).first():
            raise ValidationError('Email is a unique field')
        return True

