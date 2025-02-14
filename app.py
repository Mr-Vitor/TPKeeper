from flask import Flask
from models.config import init_db


app = Flask(__name__)

init_db(app)

@app.route('/')
def index():
    return "oi"
