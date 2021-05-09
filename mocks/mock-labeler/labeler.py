import os
import logging

from pythonjsonlogger import jsonlogger
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
scheduler = APScheduler()
scheduler.init_app(app)

structured_logger = logging.getLogger(__name__)


@app.route('/start')
def start_bot():
    return 'Start the Mock Labeler'


def label_feedback_data():
    unlabeled_data = db.feedback_data.find({'ground_truth': {'$exists': False}})
    for unlabeled_data_point in unlabeled_data:
        unseen_data_point = db.unseen_data.find_one({'id': unlabeled_data_point['id']})
        unlabeled_data_point['ground_truth'] = unseen_data_point['popularity']
        structured_logger.info({
                'message': 'Error computation',
                'abs_error': float(abs(unlabeled_data_point['ground_truth'] - unlabeled_data_point['prediction']))
            })
        db.feedback_data.replace_one({'_id': unlabeled_data_point['_id']}, unlabeled_data_point)


def setup_logging(log_level):
    logger = logging.getLogger()
    logger.setLevel(log_level)
    json_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        fmt='%(asctime)s %(message)s %(levelname)s %(name)s %(filename)s %(funcName)s'
    )
    json_handler.setFormatter(formatter)
    logger.addHandler(json_handler)


if __name__ == '__main__':
    setup_logging('INFO')

    port = app.config.get('PORT')

    scheduler.add_job('label_data', label_feedback_data, trigger='interval', seconds=10)

    # Start scheduler
    scheduler.start()

    # Reloader is disabled in order to not run code twice on start up
    app.run(host=app.config.get('HOST'), port=port, use_reloader=False)
