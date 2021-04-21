from sqlalchemy.sql import func
from slugify import slugify
from flask_login import UserMixin

from .cache import SaveCache
from .config.extensions import db, login_manager


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


class Tag(SaveMixin, db.Model):
    title = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return self.title

    def __init__(self, title):
        self.title = title


class Category(SaveMixin, db.Model):
    title = db.Column(db.String(80), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    recipes = db.relationship('Recipe', backref=db.backref('category', lazy=True))

    is_published = db.Column(db.Boolean(), default=True)

    def __repr__(self):
        return self.title

    def __init__(self, title, image):
        self.title = title
        self.image = image


recipe_tag_relation = db.Table('recipe_tag_relation', db.Model.metadata,
                               db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
                               db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                               )


class User(UserMixin, SaveMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=False)
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(150), nullable=True)
    email = db.Column(db.String(254), nullable=False)
    username = db.Column(db.String(150), nullable=False)

    is_active = db.Column(db.Boolean, nullable=False, default=False)
    date_joined = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    bio = db.Column(db.TEXT, nullable=True)
    image = db.Column(db.String(500), nullable=True)
    is_superuser = db.Column(db.Boolean, nullable=False, default=False)
    recipes = db.relationship('Recipe', backref=db.backref('owner', lazy=True))

    def __init__(self, id, email, username, first_name=None, last_name=None, bio=None,
                 image=None, is_active=False, date_joined=None, is_superuser=False):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.is_active = is_active
        self.bio = bio
        self.image = image
        self.date_joined = date_joined
        self.is_superuser = is_superuser

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


class Recipe(SaveMixin, db.Model):
    # relation's
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
                            nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                         nullable=False)
    tags = db.relationship('Tag', secondary=recipe_tag_relation,
                           backref=db.backref('tags', lazy=True))
    slug = db.Column(db.String(120), nullable=False)

    # information's
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=True)

    is_published = db.Column(db.Boolean(), default=True)

    def __repr__(self):
        return self.title

    def __init__(self, title, description, short_description, category_id, owner_id=32, image='',
                 is_published=True, **kwargs):
        self.slug = slugify(title)
        self.title = title
        self.image = image
        self.description = description
        self.short_description = short_description
        self.category_id = category_id
        owner = User.query.filter_by(id=owner_id).first()
        self.owner_id = owner
        self.is_published = is_published

    def save(self):
        super().save()
        new_recipe_data = self.to_dict()
        SaveCache(new_post=new_recipe_data)

    def to_dict(self):
        from .schemas.schemas import RecipeSchema
        return RecipeSchema().dumps(self)
