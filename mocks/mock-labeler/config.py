"""Flask configuration."""
from os import environ


class Config:
    """Base config."""
    # Flask-APScheduler comes with a build-in API
    SCHEDULER_API_ENABLED = True


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    MONGO_URI = 'mongodb://mongodb:27017/songdb'
    HOST = '0.0.0.0'
    PORT = 2002


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    MONGO_URI = 'mongodb://localhost:27017/songdb'
    HOST = 'localhost'
    PORT = 2002
