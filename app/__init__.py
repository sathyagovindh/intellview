from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_session import Session
import os

mongo = PyMongo()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)

    app.secret_key = os.environ.get('SECRET_KEY')  # Read secret key from environment variable
    app.config['MONGO_URI'] = os.environ.get('MONGO_URI')  # Read Mongo URI from environment variable
    app.config['SESSION_TYPE'] = 'filesystem'

    mongo.init_app(app)
    bcrypt.init_app(app)
    Session(app)

    # 🔁 Move this import *inside* the function
    from .views import main_bp
    app.register_blueprint(main_bp)

    return app
