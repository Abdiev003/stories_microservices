from http import HTTPStatus

from flask import send_from_directory, request, jsonify, session
from marshmallow import ValidationError

from ..config.extensions import MEDIA_ROOT, db
from ..utils.commons import save_file
from ..schemas.schemas import RecipeSchema
from ..models import Recipe
from slugify import slugify

from ..app import app


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(MEDIA_ROOT, filename)


@app.route('/recipes/', methods=['GET', 'POST'])
def recipes():
    if request.method == 'POST':
        try:
            data = dict(request.json or request.form)
            image = request.files.get('image')
            recipe = RecipeSchema().load(data)
            recipe.owner_id = 1
            recipe.image = save_file(image)
            recipe.save()
            return RecipeSchema().jsonify(recipe), HTTPStatus.CREATED
        except ValidationError as err:
            return jsonify(err.messages), HTTPStatus.BAD_REQUEST
    recipes = Recipe.query.filter_by(is_published=True)
    return RecipeSchema(many=True).jsonify(recipes), HTTPStatus.OK


@app.route('/recipes/<int:recipe_id>/', methods=['GET', 'PATCH', 'DELETE'])
def recipe_detail(recipe_id):
    if request.method == 'PATCH':
        title = request.json.get('title')
        short_description = request.json.get('short_description')
        description = request.json.get('description')
        category = request.json.get('category')
        image = request.files.get('image')
        recipe = Recipe.query.filter_by(id=recipe_id).first()

        if title:
            recipe.title = title
            recipe.slug = slugify(title)
        if short_description:
            recipe.short_description = short_description
        if description:
            recipe.description = description
        if category:
            recipe.category_id = category
        if image:
            recipe.image = image
        db.session.add(recipe)
        db.session.commit()
        return RecipeSchema().jsonify(recipe), HTTPStatus.OK

    elif request.method == 'DELETE':
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        recipe.delete()
        return jsonify({'message': 'success'}), HTTPStatus.NO_CONTENT

    recipe = Recipe.query.filter_by(id=recipe_id, is_published=True).first()
    if not recipe:
        return jsonify({'detail': 'Not found'})
    return RecipeSchema().jsonify(recipe), HTTPStatus.OK
