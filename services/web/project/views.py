"""
This file contains all the routes for the Flask app.
"""

from flask import render_template

from project import app
from project import forms

@app.route("/")
def home():
    return render_template("home.html")


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


#Start of an app route for a user profile
# @app.route("/user-profile/<user_id>")
# def show_profile(user_id):
#     """Show a user's profile with their account info"""
    #PSEUDOCODE--

    #get user_id from sessions
    #if we are logged in, get user's info from db and display on page
        #return render_template("user-profile.html", #add data we want to display in Jinja)
    #if we are not logged in...
        #flash("Access Denied. Register an account to access this page!")
        #return redirect("/")
