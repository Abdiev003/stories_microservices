import os
import redis

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

from ..app import app

BASE_DIRS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIRS, 'media')


class RedisConfig:
    HOST = os.environ.get('REDIS_HOST', 'localhost')
    PORT = os.environ.get('REDIS_PORT', 6379)
    CHANNEL_NAME = 'events'
    PASSWORD = os.environ.get('REDIS_PASSWORD', '1234')

    @property
    def client(self):
        return redis.Redis(host=self.HOST, port=self.PORT, password=self.PASSWORD, db=0)


app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://db_user:123@127.0.0.1:5434/db_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['CELERY_BROKER_URL'] = "redis://:1234@localhost:6379/0"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
