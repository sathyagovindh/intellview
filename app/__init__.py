from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_session import Session

mongo = PyMongo()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)

    app.secret_key = 'your_secret_key'
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/mock_interview'
    app.config['SESSION_TYPE'] = 'filesystem'

    mongo.init_app(app)
    bcrypt.init_app(app)
    Session(app)

    # 🔁 Move this import *inside* the function
    from .views import main_bp
    app.register_blueprint(main_bp)

    return app
