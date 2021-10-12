"""
This file contains all the routes for the Flask app.
"""

from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user

from project import app
from project import db
from project import forms
from project import models
from project import helpers


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/events/create-event', methods=['GET', 'POST'])
@login_required
def create_event():
    if current_user.user_type != 'admin':
        flash("You do not have permission to create events.")
        return redirect('/events')
    form = forms.CreateEventForm()
    print(form.data)
    if form.validate_on_submit():
        print('Adding event to DB...')
        event = models.Event(
            start_utc = form.start.data,
            end_utc = form.end.data,
            title = form.title.data,
            description = form.description.data,
            restrict_by_zipcode = form.restrict_attendees.data
        )
        db.session.add(event)
        db.session.commit()

        event_id = event.id
        user_id = current_user.get_id()

        # Add event creator to attendee list
        attendee = models.EventAttendees(
            event_id = event_id,
            attendee_id = user_id,
            rsvp_at = datetime.now()
        )
        db.session.add(attendee)
        db.session.commit()

        # make event creator an admin for event
        admin = models.EventAdmin(
            user_id = user_id,
            event_id = event_id
        )
        db.session.add(admin)
        db.session.commit()

        # handling tags as comma-separated string
        tags_string: str = form.tags.data
        tags_list: list = tags_string.split(',')
        for tag in tags_list:
            clean_tag = tag.strip()
            event_tag= models.EventTags(
                tag = clean_tag,
                event_id = event_id
            )
            db.session.add(event_tag)
            db.session.commit()
        
        # add event attendees from email list
        attendees_string = form.attendee_emails.data
        attendees_list: list = attendees_string.split(',')
        for email in attendees_list:
            clean_email = email.strip()
            invite_user = models.User.query.filter(models.User.email == clean_email).first()
            # TODO: notify user if email doesn't match email from user in our DB
            if invite_user:
                invite_attendee = models.EventAttendees(
                    event_id = event_id,
                    attendee_id = invite_user.id,
                    rsvp_at = datetime.now()
                )
                db.session.add(invite_attendee)
                db.session.commit()

        # handle zip code restrictions
        if form.restrict_attendees.data:
            zipcode_string = form.zipcodes.data
            zipcode_list = zipcode_string.split(',')
            for zipcode in zipcode_list:
                clean_zipcode = zipcode.strip()
                if len(clean_zipcode) == 5:
                    # TODO: notify user if zip code is not valid
                    eligible_zipcode = models.EventEligibleZipcode(
                        zipcode = clean_zipcode,
                        event_id = event_id
                    )
                    db.session.add(eligible_zipcode)
                    db.session.commit()
        
        
        
        print('Event successfully added to DB.')
        return redirect('/events')
    return render_template('create_event.html', form=form)


@app.route('/events', methods=["GET", "POST"])
def view_events():
    events = helpers.get_future_events()
    form = forms.RSVPForm()

    if request.method == "POST":
        if not current_user.is_authenticated:
            flash('You must be logged in to RSVP.')
        else:
            flash("You are now RSVP'd to this event.")
            event_id = request.form.get("rsvp")
            event = helpers.get_event_by_id(event_id)

            # Checking if user has already RSVP'd
            user_id = current_user.get_id()
            future_events = helpers.get_future_user_events(user_id)
            if event in future_events:
                flash("You have already RSVD'd to this event.")
            else:
            # Add RSVP if they have not already RSVP'd
                rsvp = models.EventAttendees(
                                event_id=event_id,
                                attendee_id=user_id,
                                rsvp_at=datetime.now()
                                )
                db.session.add(rsvp)
                db.session.commit()
    return render_template('events.html', events=events, form=form)


@app.route('/events/<int:event_id>', methods=["GET", "POST"])
def view_event_details(event_id: int):
    event = models.Event.query.get(event_id)
    events = helpers.get_future_events()
    form = forms.RSVPForm()

    if request.method == "POST":
        if not current_user.is_authenticated:
            flash('You must be logged in to RSVP.')
        else:
            flash("You are now RSVP'd to this event.")
            event_id = request.form.get("rsvp")
            event = helpers.get_event_by_id(event_id)

            # Checking if user has already RSVP'd
            user_id = current_user.get_id()
            future_events = helpers.get_future_user_events(user_id)
            if event in future_events:
                flash("You have already RSVD'd to this event.")
            else:
            # Add RSVP if they have not already RSVP'd
                rsvp = models.EventAttendees(
                                event_id=event_id,
                                attendee_id=user_id,
                                rsvp_at=datetime.now()
                                )
                db.session.add(rsvp)
                db.session.commit()
    return render_template('event_details.html', event=event, form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = forms.LoginForm()
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = models.User.query.filter_by(email=email).first()
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

        if models.User.query.filter_by(email=request.form.get('email')).first():
            #User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = models.User(
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
    
    #TODO: implement current_user from flask_login extension to only make the logged in user's profile editable
        # https://flask-login.readthedocs.io/en/latest/#flask_login.current_user 
    return render_template("user-profile.html", user=user, events=attended_events)


@app.route("/all-users")
@login_required
def show_all_users(): 
    """Show list of all users"""

    users = models.User.query.all()
    
    return render_template("all-users.html", users=users)



