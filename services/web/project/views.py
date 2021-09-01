"""
This file contains all the routes for the Flask app.
"""
from project import app

@app.route('/')
def index():
    return 'Hello World!'