from flask import Flask
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(16).hex()

from auth import main
