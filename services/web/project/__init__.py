
"""
This file is used to instantiate the Flask app.
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from project import forms
app = Flask(__name__, template_folder='templates')
app.config.from_object("project.config.Config")
app.secret_key = "any-string"
Bootstrap(app)
db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = forms.LoginForm()
    if login_form.validate_on_submit():
        if login_form.email.data == "admin@email.com" and login_form.password.data == "12345678":
            return render_template("success.html")
        else:
            return render_template("denied.html")
    return render_template('login.html', form=login_form)


@app.route("/register", methods=["GET", "POST"])
def register():
    registration_form = forms.RegistrationForm()
    # if registration_form.validate_on_submit():
    return render_template('register.html', form=registration_form)
# while it is usually better to do all imports at the top of the file, importing here mid-file is a best practice for Flask
from project import models  
from project import views
