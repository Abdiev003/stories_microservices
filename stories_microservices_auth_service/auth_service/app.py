from flask import Flask

app = Flask(__name__)

from .config.extensions import *
from .models import *
from .api.routers import *

if __name__ == '__main__':
    app.run(debug=True, port=5002)
