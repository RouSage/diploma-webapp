from flask import Flask
from config import BaseConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, static_folder='static')
app.config.from_object(BaseConfig)
db = SQLAlchemy(app=app)
migrate = Migrate(app=app, db=db)

from app import routes, models
