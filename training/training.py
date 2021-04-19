from pycaret.regression import *
from pymongo import MongoClient
import pandas as pd
import mlflow

# set tracking uri
mlflow.set_tracking_uri('http://localhost:5000')

# build a new client instance for MongoClient
mongo_client = MongoClient('localhost', 27017)

# create new database and client collection
db = mongo_client.songdb
col = db.training_data

# API call to MongoDB collection
mongo_docs = col.find()

data = pd.DataFrame(list(mongo_docs))

print(data.shape)

experiment = setup(data=data,
                   ignore_features=['_id', 'id', 'artists', 'explicit', 'key', 'mode', 'name', 'release_date'],
                   log_experiment=True,
                   experiment_name='dt_v1',
                   preprocess=False,
                   target='popularity',
                   session_id=123,
                   silent=True,
                   use_gpu=True)

decision_tree = create_model('dt')

# lr = tune_model(lr)

print(decision_tree)

print(predict_model(decision_tree))

final_dt = finalize_model(decision_tree)

mlflow.sklearn.log_model(final_dt, "artifacts")
