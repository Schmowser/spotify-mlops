"""Flask configuration."""
from os import environ


class Config:
    """Base config."""


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    MONGO_URI = 'mongodb://mongodb:27017/songdb'
    HOST = '0.0.0.0'
    PORT = 9000
    MODEL_SERVICE_URI = 'http://model:8080/invocations'


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    MONGO_URI = 'mongodb://localhost:27017/songdb'
    HOST = 'localhost'
    PORT = 9000
    MODEL_SERVICE_URI = 'http://localhost:1234/invocations'
