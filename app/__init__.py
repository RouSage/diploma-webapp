import os

import config
import torch
from flask import Flask, request
from flask_babel import Babel
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.yolov3.model.yolov3_s import Yolov3_S

app = Flask(__name__, static_folder='static')

env = os.environ.get('FLASK_ENV')
if env == 'development':
    app.config.from_object(config.DevelopmentConfig)
elif env == 'production':
    app.config.from_object(config.ProductionConfig)
else:
    app.config.from_object(config.BaseConfig)

db = SQLAlchemy(app=app)
migrate = Migrate(app=app, db=db)
babel = Babel(app=app)

# Load exesting model to CPU and load weights
model = Yolov3_S()
model.load_state_dict(torch.load(f=os.path.join(
    app.static_folder, app.config['TRAINED_MODEL_NAME']), map_location='cpu'))


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])


from app import models, routes
