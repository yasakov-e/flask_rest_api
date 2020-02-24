from time import time
from flask import jsonify
from config import app


def health():
    """
    This function responds to the URL
    localhost/health
    """
    app_run_time = time() - app.config.app_start_time

    return jsonify(status='200 OK',
                   application_run_time=f'{round(app_run_time, 2)} seconds')
