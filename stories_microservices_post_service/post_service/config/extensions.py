import os

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flasgger import Swagger

from ..app import app


BASE_DIRS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIRS, 'media')

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://db_user:123@127.0.0.1:5432/db_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
ma = Marshmallow(app)
swagger = Swagger(app)
