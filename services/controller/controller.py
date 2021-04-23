import json
import os
import requests

from flask import Flask, request
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


@app.route('/predict', methods=['POST'])
def start_bot():
    request_data = request.get_json()

    headers = {
        'Content-Type': 'application/json',
        'format': 'pandas-split'
    }
    body = {
        'columns': [
            list(request_data.keys())
        ],
        'data': [
            list(request_data.values())
        ]
    }

    response = requests.post('http://localhost:1234/invocations',
                             data=json.dumps(body),
                             headers=headers)

    db.feedback_data.insert_one(request_data)

    return response.content


if __name__ == '__main__':
    port = app.config.get('PORT')

    # reloader is disabled in order to not run code twice on start up
    app.run(host=app.config.get('HOST'), port=port, use_reloader=False)
