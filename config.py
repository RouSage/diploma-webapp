import os


basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', default='default-secret-key')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TRAINED_MODEL_NAME = os.environ.get(
        'TRAINED_MODEL_NAME', default='trained_model.pt')

    LANGUAGES = ['en', 'ru']


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
