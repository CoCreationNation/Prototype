
"""
This file is used to instantiate the Flask app.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from project.momentjs import momentjs



app = Flask(__name__, template_folder='templates')
app.config.from_object("project.config.Config")
app.jinja_env.globals['momentjs'] = momentjs
Bootstrap(app)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)


# while it is usually better to do all imports at the top of the file, importing here mid-file is a best practice for Flask
from project import models  
from project import views
from project import forms
