from ..config.extensions import ma

from flask_marshmallow.fields import AbsoluteURLFor
from marshmallow import validates, ValidationError, fields

from ..models import Recipe, Category, User


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        include_fk = True


class UserSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = User
        include_fk = True


class RecipeSchema(ma.SQLAlchemyAutoSchema):
    image = AbsoluteURLFor(
        'uploaded_file',
        filename='<image>'
    )
    slug = fields.String(attribute="slug", dump_only=True)
    owner = fields.Method('get_owner', dump_only=True)
    category = fields.Method('get_category', dump_only=True)
    category_id = fields.Integer(attribute='category_id', required=True, load_only=True)

    class Meta:
        model = Recipe
        include_fk = True
        load_instance = True
        exclude = (
            'owner_id',
        )

    @validates('category_id')
    def validate_category_id(self, category_id):
        category = Category.query.filter_by(id=category_id).first()
        if not category:
            raise ValidationError("Category not found")


    def get_owner(self, recipe):
        return UserSchema().dump(recipe.owner)

    def get_category(self, recipe):
        return CategorySchema().dump(recipe.category)