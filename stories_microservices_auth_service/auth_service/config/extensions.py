import os
import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flasgger import Swagger


from ..app import app


BASE_DIRS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIRS, 'media')

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://auth_db_user:123@127.0.0.1:5433/auth_db_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=10)


db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
swagger = Swagger(app)