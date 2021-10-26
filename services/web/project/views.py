"""
This file contains all the routes for the Flask app.
"""

from datetime import datetime
import os

#from typing_extensions import Required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from flask import render_template, request, url_for, redirect, flash, abort, jsonify
from flask_wtf.csrf import CSRFProtect
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
import pytz
from twilio.base.exceptions import TwilioRestException
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant, ChatGrant

from project import app
from project import db
from project import forms
from project import models
from project import helpers
from project import token
from project import email

login_manager = LoginManager(app)
login_manager.login_view = "login"

csrf = CSRFProtect()

twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
twilio_api_key_sid = os.environ.get('TWILIO_API_KEY_SID')
twilio_api_key_secret = os.environ.get('TWILIO_API_KEY_SECRET')


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    
    if user_id is not None:
        return models.User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    
    flash('You must be logged in to view that page.')
    return redirect("/login")


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
            start_utc = helpers.convert_dateime_to_utc(form.start.data, form.timezone.data),
            end_utc = helpers.convert_dateime_to_utc(form.end.data, form.timezone.data),
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
            event_tag = models.EventTags(
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
    events_by_three = helpers.group_list_by_threes(events)
    
    user_events = helpers.get_future_user_events(current_user.id) if current_user.is_authenticated else []

    form = forms.RSVPForm()

    if request.method == "POST":
        if not current_user.is_authenticated:
            flash('You must be logged in to RSVP.')
            return redirect("/login")
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
    return render_template('events.html', events_by_three=events_by_three, user_events=user_events, form=form)


@app.route('/events/<int:event_id>', methods=["GET", "POST"])
def view_event_details(event_id: int):
    event = models.Event.query.get(event_id)
    event_tags = models.EventTags.query.filter_by(event_id = event_id).all()
    event_tags_items = [tag.tag for tag in event_tags]
    final_list_tags = ",".join(event_tags_items) #list to string conversion
    eligible_zipcodes = models.EventEligibleZipcode.query.filter_by(event_id = event_id).all()
    zipcode_items = [zipcode.zipcode for zipcode in eligible_zipcodes]
    final_zipcodes = ",".join(zipcode_items)
    events = helpers.get_future_events()
    form = forms.RSVPForm()

    if request.method == "POST":
        if not current_user.is_authenticated:
            flash('You must be logged in to RSVP.')
            return redirect("/login")
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
    return render_template('event_details.html', event=event, event_tags = final_list_tags, eligible_zipcodes=final_zipcodes, form=form)

@app.route('/live-event/<int:event_id>')
@login_required
def live_event(event_id):
    return render_template('event.html')


@app.route('/event_login', methods=['POST'])
def event_login():
    username = request.get_json(force=True).get('username')
    if not username:
        abort(401)

    conversation = helpers.get_chatroom('My Room')
    try:
        conversation.participants.create(identity=username)
    except TwilioRestException as exc:
        # do not error if the user is already in the conversation
        if exc.status != 409:
            raise

    token = AccessToken(twilio_account_sid, twilio_api_key_sid,
                        twilio_api_key_secret, identity=username)
    token.add_grant(VideoGrant(room='My Room'))
    token.add_grant(ChatGrant(service_sid=conversation.chat_service_sid))

    return {'token': token.to_jwt().decode(),
            'conversation_sid': conversation.sid}


@app.route('/login', methods=["GET", "POST"])
def login():
    form = forms.LoginForm()

    if current_user.is_authenticated: 
        return redirect(url_for("index"))
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
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != " ": #if no data for prev page given
                next_page = url_for("index") #just send them to home page
            
            flash(f"Welcome, {user.username}") 
            return redirect(next_page)
            
            #return redirect(url_for('index'))

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

        user_token = token.generate_confirmation_token(new_user.email)
        confirm_url = url_for('confirm_email', user_token=user_token, _external=True)
        html = render_template('email_confirmation.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        email.send_email(new_user.email, subject, html)

        return redirect(url_for("index"))

    return render_template("register.html", form=form)


@app.route('/confirm/<user_token>')
@login_required
def confirm_email(user_token):
    print('token:', user_token)
    try:
        email = token.confirm_token(user_token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('index'))
    print('querying user...')
    user = models.User.query.filter_by(email=email).first_or_404()
    if user.email_confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.email_confirmed = True
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('index'))


@app.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))


@app.route('/user-profile/<user_id>')
@login_required
def show_profile(user_id):
    """Show a user's profile with their account info"""
    
    user = helpers.get_user_info(user_id) 
    attended_events = helpers.get_user_events(user_id)
    user_in_session = current_user

    return render_template("user-profile.html", user=user, events=attended_events, user_in_session=user_in_session)

@app.route('/edit-profile/<user_id>', methods=["GET", "POST"])
@login_required
def edit_profile(user_id): 
    """Gather and save edited info to signed in user"""

    form = forms.RegistrationForm()

    first_name = form.first_name.data 
    last_name = form.last_name.data
    pronouns = form.pronouns.data
    address_1 = form.address_1.data
    city = form.city.data
    state = form.state.data
    zip_code = form.zip_code.data
    phone_number = form.phone_number.data

    if request.method == "POST": 
        user = helpers.update_user_details(user_id, first_name, last_name,
                                           pronouns, address_1, city, state, zip_code, phone_number)
        return redirect("/user-profile/" + str(user_id))

    user = helpers.get_user_info(user_id)
    
    #TODO: Allow user to update their email/username(?) and add check for dupe usernames/email validation

    return render_template("edit-profile.html",  user=user, form=form)

@app.route("/all-users")
@login_required
def show_all_users(): 
    """Show list of all users"""

    form = forms.DeleteUserForm()
    users = models.User.query.all()
    
    return render_template("all-users.html", users=users, form=form)

@app.route('/delete-user/<int:user_id>', methods=["GET", "POST"])
@login_required
def delete_user(user_id):
    """Admin privilege to delete user."""

    users = models.User.query.all()
    if current_user.user_type != 'admin':
        flash('You do not have permission to delete users.')
    form = forms.DeleteUserForm()
    if request.method == "POST":
        user = request.form.get('delete-user')
        helpers.delete_user(user)
        db.session.commit()
        flash('User has been deleted.')
        return render_template("all-users.html", form=form, user=user)
    else:
        render_template("all-users.html", users=users, form=form)


@app.route('/about-us')
def about_us():
    return render_template("about-us.html") 

