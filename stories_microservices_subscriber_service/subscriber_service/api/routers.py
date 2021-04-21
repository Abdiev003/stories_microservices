from http import HTTPStatus
from flask import request, jsonify
from marshmallow import ValidationError

from ..schemas.schemas import SubscriberSchema
from ..app import app


@app.route('/subscribe/', methods=['POST'])
def subscribe():
    data = dict(request.json or request.form)
    try:
        subscriber = SubscriberSchema().load(data)
    except ValidationError as err:
        return err.messages, 400
    subscriber.save()
    return SubscriberSchema().jsonify(subscriber), HTTPStatus.CREATED

