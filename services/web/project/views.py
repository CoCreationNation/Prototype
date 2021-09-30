"""
This file contains all the routes for the Flask app.
"""


from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user

from project import app
from project import db
from project import forms
from project import db
from project.models import User
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


@app.route('/login', methods=["GET", "POST"])
def login():
    form = forms.LoginForm()
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        # Email exists and password correct
        else:
            login_user(user)
            flash(f"Welcome, {user.username}")
            return redirect(url_for('index'))

    return render_template("login.html", form=form)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = forms.RegistrationForm()
    if request.method == "POST":

        if User.query.filter_by(email=request.form.get('email')).first():
            #User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=request.form.get('email'),
            username=request.form.get('username'),
            password=hash_and_salted_password,
            zip_code=request.form.get('zip_code')
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash('Your account has been registered.')
        return redirect(url_for("index"))

    return render_template("register.html", form=form)


@app.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))


@app.route("/user-profile/<user_id>")
@login_required
def show_profile(user_id):
    """Show a user's profile with their account info"""
    
    user = helpers.get_user_info(user_id) 
    attended_events = helpers.get_user_events(user_id)
    user_in_session = current_user
    
    #TODO: implement current_user from flask_login extension to only make the logged in user's profile editable
        # https://flask-login.readthedocs.io/en/latest/#flask_login.current_user 
    return render_template("user-profile.html", user=user, events=attended_events, user_in_session=user_in_session)


@app.route("/all-users")
@login_required
def show_all_users(): 
    """Show list of all users"""

    users = User.query.all()
    
    return render_template("all-users.html", users=users)