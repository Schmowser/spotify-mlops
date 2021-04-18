import json
import os
import requests

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
    # Call the model service TODO: Pass Payload to this endpoint to model service
    headers = {
        'Content-Type': 'application/json',
        'format': 'pandas-split'
    }
    body = {
        'data': [
            [0.8109999999999999, 0.498, 185320, 0.47100000000000003,
             0.113, 0.121, -10.405999999999999, 0.0411,
             112.01799999999999, 0.35100000000000003, 2020]
        ]
    }
    response = requests.post('http://localhost:1234/invocations',
                             data=json.dumps(body),
                             headers=headers)
    return response.content


if __name__ == '__main__':
    port = app.config.get('PORT')

    # reloader is disabled in order to not run code twice on start up
    app.run(host=app.config.get('HOST'), port=port, use_reloader=False)
