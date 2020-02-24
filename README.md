### Simple Flask REST API

### Setup

Install dependencies:
`pip install -r requirements.txt`

Run application locally:
`gunicorn --bind 0.0.0.0:5000 --log-config logging.conf server:connexion_app`

Swagger documentation for API is available on:
`localhost/ui`

Application logs could be found here:
`app_dir/log/application.log`

### Run application in Docker
Pull the image from docker-hub:
`docker pull eugeneyasakov/python_rest_api:latest`

Run the container:
`docker run -p 80:8000 eugeneyasakov/python_rest_api`

App should be available on your localhost.