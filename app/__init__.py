import os
import torch
from flask import Flask, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
import config
from app.utils import CNN

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

# Load exesting model to CPU and set model to evaluation mode
model = CNN()
model.load_state_dict(torch.load(
    f=os.path.join(app.static_folder, app.config['TRAINED_MODEL_NAME']),
    map_location='cpu'))
model.eval()


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])


from app import models, routes
