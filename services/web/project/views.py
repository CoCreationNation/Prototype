"""
This file contains all the routes for the Flask app.
"""

from flask import render_template, redirect

from project import app
from project import db
from project import forms
from project import models
from project import helpers


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/events/create-event', methods=['GET', 'POST'])
def create_event():
    form = forms.CreateEventForm()
    print(form.data)
    if form.validate_on_submit():
        print('Adding event to DB...')
        event = models.Event(
            start_utc = form.start.data,
            end_utc = form.end.data,
            title = form.title.data,
            description = form.description.data
        )
        db.session.add(event)
        db.session.commit()
        print('Event successfully added to DB.')
        return redirect('/events')
    return render_template('create_event.html', form=form)


@app.route('/events')
def view_events():
    events = helpers.get_future_events()
    return render_template('events.html', events=events)


@app.route('/events/<int:event_id>')
def view_event_details(event_id: int):
    event = models.Event.query.get(event_id)
    return render_template('event_details.html', event=event)


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


@app.route("/user-profile/") #eventually should be ("/user-profile/<user_id>")
def show_profile():
    """Show a user's profile with their account info"""
    return render_template("user-profile.html")
    
    #PSEUDOCODE--

    #get user_id from sessions
    #if we are logged in, get user's info from db and display on page
        #return render_template("user-profile.html", + data we want to display in Jinja)
    #if we are not logged in...
        #flash("Access Denied. Register an account to access this page!")
        #return redirect("/")
