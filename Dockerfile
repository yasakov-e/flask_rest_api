FROM python:3.8.1

COPY . /flask_rest_api

WORKDIR /flask_rest_api

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "2", "--log-config", "logging.conf", "server:connexion_app"]