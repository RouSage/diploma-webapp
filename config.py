import os


basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'production'
    DEBUG = os.environ.get('DEBUG') or False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-secret-key'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') \
        or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TRAINED_MODEL_NAME = os.environ.get('TRAINED_MODEL_NAME')
