import os

from flask import Flask
from flask_pymongo import PyMongo


app = Flask(__name__)
mode = os.environ.get('FLASK_ENV')
if mode == 'production':
    app.config.from_object('config.ProdConfig')
elif mode == 'development':
    app.config.from_object('config.DevConfig')
else:
    app.config.from_object('config.DevConfig')

# Configure MongoDB
mongo = PyMongo(app)
db = mongo.db


@app.route('/')
def start_bot():
    return 'Test'


if __name__ == '__main__':
    port = app.config.get('PORT')

    # reloader is disabled in order to not run code twice on start up
    app.run(host=app.config.get('HOST'), port=port, use_reloader=False)
