import torch
import os
from flask import Flask
import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
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

# Load exesting model to CPU and set model to evaluation mode
model = CNN()
model.load_state_dict(torch.load(
    f=os.path.join(app.static_folder, app.config['TRAINED_MODEL_NAME']),
    map_location='cpu'))
model.eval()

from app import routes, models
