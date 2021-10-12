
"""
This file is used to instantiate the Flask app.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap


app = Flask(__name__, template_folder='templates')
app.config.from_object("project.config.Config")
Bootstrap(app)
db = SQLAlchemy(app)
# csrf = CSRFProtect(app) # TODO: add CSRF token through JavaScript. https://stackoverflow.com/questions/22854749/flask-and-ajax-post-http-400-bad-request-error


# while it is usually better to do all imports at the top of the file, importing here mid-file is a best practice for Flask
from project import models  
from project import views
from project import forms
