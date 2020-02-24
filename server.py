
from time import time
from flask import jsonify, g, request
import config

# Get the application instance
connexion_app = config.connexion_app
app = config.app

# Read the swagger.yml file to configure the endpoints
connexion_app.add_api("swagger.yml")

# Measure app start time for /health endpoint
app.config.app_start_time = time()


@app.before_request
def take_start_time():
    g.start = time()


@app.after_request
def log_request(response):
    if not request.path.startswith(config.REQUESTS_TO_TIME):
        return response

    diff = time() - g.start

    request_string = "%s %s" % (request.method, request.url)
    time_string = "%f seconds" % diff

    app.logger.info(
        '',
        extra={
            'request': request_string,
            'request_duration': time_string})
    return response


if __name__ == "__main__":
    connexion_app.run(debug=True)
