import json
import os
import requests

from flask import Flask
from flask_pymongo import PyMongo
from flask_apscheduler import APScheduler


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

# Define Flask APScheduler to have recurring tasks scheduled and executed
scheduler = APScheduler()  # TODO: Do we need a job store to persist information on running jobs?
scheduler.init_app(app)


@app.route('/start')
def start_bot():
    return 'Start the Mock Caller'


def fetch_unseen_data_and_get_prediction():
    something = list(db.unseen_data.aggregate([{'$sample': {'size': 1}}]))
    request_body = something[0]
    for key in ['_id', 'id', 'artists', 'explicit', 'key', 'mode', 'name', 'release_date', 'popularity']:
        del request_body[key]
    print(request_body)

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post('http://localhost:9000/predict',
                             data=json.dumps(request_body),
                             headers=headers)
    print(response.content)


if __name__ == '__main__':
    port = app.config.get('PORT')

    scheduler.add_job('perform_unseen_call', fetch_unseen_data_and_get_prediction, trigger='interval', seconds=10)

    # Start scheduler
    scheduler.start()

    # Reloader is disabled in order to not run code twice on start up
    app.run(host=app.config.get('HOST'), port=port, use_reloader=False)
