# spotify-mlops
Showcase of monitoring and retraining of Machine Learning model on Spotify data

## Data

[Data Source](https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks)
split into
* Training Data (1921 - 1991)
* Feedback Data (1992 - 2021)

## Services

### Controller

## Mocks

### Mock Caller

### Mock Labeler

### How to run the application

##### Required packages

Install following packages via pip (make sure to use pip3):
* `pip install flask` (APIs)
* `pip install Flask-APScheduler` (Job Scheduler for Flask with API)
* `pip install Flask-PyMongo` (MongoDB Wrapper)
* `pip install pycaret` (AutoML framework for model training)
* `pip install python-json-logger` (Structured logging for monitoring - ELK)

#### Set up database

The application requires a NoSQL database. For local development run a MongoDB instance on port 27017. 
A convenient way would be running a Docker container of the official MongoDB image. You can pull the latest image via
`docker pull mongo`
and run a container with
`docker run -d -p 27017:27017 --name retarddb mongo`.

Run the `import-data.sh` script in order to fill mongodb with data. It requires to have the CSV files of the Kaggle dataset 
in a folder `data`.

#### Running the application

* In IntelliJ IDEA / PyCharm: Right-click on `main.py` and select `▶️ Run`.
* From the command line: Navigate to `cd src`, specify the app name and the environment `export FLASK_APP=main`, 
`export FLASK_ENV=development` or `export FLASK_ENV=production`. Finally, run flask `flask run`.
  
With `FLASK_ENV=development` the application starts on `localhost:9000`.
With `FLASK_ENV=production` the application starts on `0.0.0.0:9000`.

In order to start all services and mocks, use the docker-compose.yml by running after building all relevant Docker Images
```
docker compose up
```

## Experiment Tracking

In order to track experiment, we integrate MLFlow. For local usage please, navigate into the `traning` folder and start 
an MLFlow server which can be reached at `localhost:5000`

```
cd training
mlflow ui
```

## Serving the model

Locally from command line
```
mlflow models serve -m runs:/<RUN_ID>/artifacts -p 1234
```

Build the docker image and run a container exposing the service on port 1234
```
mlflow models build-docker -m runs:/<RUN_ID>/artifacts -n <IMAGE_NAME>
docker run -p 1234:8080 <IMAGE_NAME>
```

## Specification

### Example Request

```
curl --location --request POST 'localhost:9000/predict' \
--header 'Content-Type: application/json' \
--data-raw '{
    "acousticness": 0.8109999999999999,
    "danceability": 0.498,
    "duration_ms": 185320,
    "energy": 0.47100000000000003,
    "instrumentalness": 0.113,
    "liveness": 0.121,
    "loudness": -10.405999999999999,
    "speechiness": 0.0411,
    "tempo": 112.01799999999999,
    "valence": 0.35100000000000003,
    "year": 2020,
    "id": "5BK0uqwY9DNfZ630STAEaq"
}'
```

### Example Response

```
68.0
```

