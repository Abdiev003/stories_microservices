import os
import datetime
import redis

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flasgger import Swagger

from ..app import app

BASE_DIRS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIRS, 'media')


class RedisConfig:
    HOST = os.environ.get('HOST', 'localhost')
    PORT = os.environ.get('PORT', 6379)
    CHANNEL_NAME = 'events'
    PASSWORD = os.environ.get('PASSWORD', '1234')

    @classmethod
    def client(cls):
        return redis.Redis(host=cls.HOST, port=cls.PORT, password=cls.PASSWORD, db=0)


app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://auth_db_user:123@127.0.0.1:5433/auth_db_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config['SECRET_KEY'] = 'dsasdnmrjuihrewn'
app.config['SECURITY_PASSWORD_SALT'] = 'My_Salt'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=10)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
swagger = Swagger(app)
