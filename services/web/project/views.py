"""
This file contains all the routes for the Flask app.
"""
from flask import render_template

from project import app

@app.route('/')
def index():
    return render_template('home.html')