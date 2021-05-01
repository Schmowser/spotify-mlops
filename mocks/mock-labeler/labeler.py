import os

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


@app.route('/start')
def start_bot():
    return 'Start the Mock Labeler'


def label_feedback_data():
    unlabeled_data = db.feedback_data.find({'ground_truth': {'$exists': False}})
    for unlabeled_data_point in unlabeled_data:
        print(unlabeled_data_point)
        unseen_data_point = db.unseen_data.find_one({'id': unlabeled_data_point['id']})
        print(unseen_data_point['popularity'])
        unlabeled_data_point['ground_truth'] = unseen_data_point['popularity']
        db.feedback_data.replace_one({'_id': unlabeled_data_point['_id']}, unlabeled_data_point)


if __name__ == '__main__':
    port = app.config.get('PORT')

    scheduler.add_job('label_data', label_feedback_data, trigger='interval', seconds=10)

    # Start scheduler
    scheduler.start()

    # Reloader is disabled in order to not run code twice on start up
    app.run(host=app.config.get('HOST'), port=port, use_reloader=False)
