from http import HTTPStatus

from flask import send_from_directory, request, jsonify, session
from marshmallow import ValidationError
from flasgger import swag_from


from ..config.extensions import MEDIA_ROOT, db
from ..models import User
from ..schemas.schemas import UserSchema
from ..utils.commons import save_file
from ..utils.tokens import confirm_token
from werkzeug.security import check_password_hash

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)

from ..app import app


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(MEDIA_ROOT, filename)


@app.route('/register/', methods=['POST'])
@swag_from('docs/register.yml')
def register():
    try:
        data = dict(request.json or request.form)
        image = request.files.get('image')
        user = UserSchema().load(data)
        if image:
            user.image = save_file(image)
        user.save()
        user.send_confirmation_mail()
        return UserSchema().jsonify(user), HTTPStatus.CREATED
    except ValidationError as err:
        return jsonify(err.messages), HTTPStatus.BAD_REQUEST


@app.route('/confirm/<token>')
def confirm_email(token):
    email = confirm_token(token)
    if not email:
        return jsonify({'message': 'The confirmation link is invalid or has expired.'}), HTTPStatus.OK
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'Account not found'}), HTTPStatus.OK
    print('is active', user.is_active)
    if user.is_active:
        return jsonify({'message': 'Account already confirmed. Please login.'}), HTTPStatus.OK
    else:
        user.is_active = True
        user.save()
        return jsonify({'message': 'You have confirmed your account. Thanks!'}), HTTPStatus.OK


@app.route("/login/", methods=["POST"])
@swag_from('docs/login.yml')
def login():
    data = dict(request.json or request.form)
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        if not user.is_active:
            return jsonify({'message': 'Please confirm your account'}), HTTPStatus.OK
        user = UserSchema().dump(user)
        access_token = create_access_token(identity=user['id'])
        refresh_token = create_refresh_token(identity=user['id'])
        user.update({
            'access_token': access_token,
            'refresh_token': refresh_token
        })
        return jsonify(user), HTTPStatus.OK
    else:
        return jsonify({'message': 'Bad username or password'}), HTTPStatus.UNAUTHORIZED


@app.route('/user-profile/', methods=["GET"])
@jwt_required()
def user_profile():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'Not found'}), HTTPStatus.UNAUTHORIZED
    return UserSchema().jsonify(user), HTTPStatus.OK


@app.route("/protected/", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id=current_user_id).first()
    return UserSchema().jsonify(user), HTTPStatus.OK


@app.route("/refresh-token/", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    user = User.query.filter_by(id=identity).first()
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)
