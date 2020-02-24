import os
import connexion

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


REQUESTS_TO_TIME = ('/health', '/products')

basedir = os.path.abspath(os.path.dirname(__file__))

connexion_app = connexion.App(__name__, specification_dir=basedir)

app = connexion_app.app

# Build SQLite url for SQLAlchemy
sqlite_url = 'sqlite:///' + os.path.join(basedir, 'products.db')

# Configure SQLAlchemy
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create SQLAlchemy database instance
db = SQLAlchemy(app)

# Initialize Marshmallow
marshmallow = Marshmallow(app)
