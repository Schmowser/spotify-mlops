import json
import os
import requests
import logging

from pythonjsonlogger import jsonlogger
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


def setup_logging(log_level):
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    json_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        fmt='%(asctime)s %(message)s %(levelname)s %(name)s %(filename)s %(funcName)s'
    )
    json_handler.setFormatter(formatter)
    logger.addHandler(json_handler)


def setup_flask_logging():
    flask_logger = logging.getLogger()
    log_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        fmt='%(asctime)s %(message)s %(levelname)s %(name)s %(filename)s %(funcName)s'
    )
    log_handler.setFormatter(formatter)
    flask_logger.addHandler(log_handler)


@app.route('/predict', methods=['POST'])
def predict():
    logger = logging.getLogger(__name__)

    request_data_with_id = request.get_json().copy()
    request_data = request.get_json()
    del request_data['id']

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

    response = requests.post(app.config.get('MODEL_SERVICE_URI'),
                             data=json.dumps(body),
                             headers=headers)

    prediction = response.json()[0]
    request_data_with_id['prediction'] = prediction

    db.feedback_data.insert_one(request_data_with_id)
    logger.info({"prediction": str(prediction)})

    return str(prediction)


if __name__ == '__main__':
    setup_logging('INFO')
    port = app.config.get('PORT')

    # reloader is disabled in order to not run code twice on start up
    app.run(host=app.config.get('HOST'), port=port, use_reloader=False)
