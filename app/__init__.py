from flask import Flask
from flask_bootstrap import Bootstrap
from pymongo import MongoClient
from config import Config
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
Bootstrap(app)

client = MongoClient(os.getenv('MONGO_URI'))
db = client['bocotory']

# Importing and registering blueprints
from app.controllers.auth_controller import auth_bp
from app.controllers.profile_controller import profile_bp
from app.controllers.user_controller import user_bp
from app.controllers.storage_controller import storage_bp
from app.controllers.stock_controller import stock_bp
from app.controllers.supplier_controller import supplier_bp

app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(user_bp)
app.register_blueprint(storage_bp)
app.register_blueprint(stock_bp)
app.register_blueprint(supplier_bp)