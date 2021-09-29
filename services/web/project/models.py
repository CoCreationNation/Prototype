"""
This file contains all the database models for the Flask app.
"""
from sqlalchemy import sql

from project import db
from project import app
from flask_login import UserMixin, LoginManager

# for pronouns
import enum


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Pronouns(enum.Enum):
    she = "She/Her"
    he = "He/Him"
    they = "They/Them"
    other = "Other"


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)  # need to incorporate password_hash algo somehow
    user_type = db.Column(db.String)
    is_superuser = db.Column(db.Boolean(), default=False)
    username = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=True)
    first_name = db.Column(db.String, nullable=True)
    pronouns = db.Column(db.Enum(Pronouns))
    email = db.Column(db.String(128), unique=True, nullable=False)
    email_confirmed = db.Column(db.Boolean(), default=False)
    address_1 = db.Column(db.String)
    address_2 = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip_code = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<User id={self.id} email={self.email}>'  


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    start_utc = db.Column(db.DateTime(timezone=True), nullable=False)
    end_utc = db.Column(db.DateTime(timezone=True), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=sql.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=sql.func.now(), nullable=True)
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)

    #users table and events table

class EventEligibility(db.Model):
    __tablename__ = "event_eligible_attendees"

    id = db.Column(db.Integer, primary_key=True)
    event_id =db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

#users table and events table

class EventAdmin(db.Model):
    __tablename__ = "event_admins"

    id = db.Column(db.Integer, primary_key=True)
    event_id =db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    admin_level = db.Column(db.String, nullable= True) # levels are considered as "level one, two etc"


#users table and events

class EventAttendees(db.Model):
    __tablename__ = "event_attendees"

    id = db.Column(db.Integer, primary_key=True)
    event_id =db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    attendee_id =db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)   
    rsvp_at =db.Column(db.DateTime(timezone=True)) # time the user rsvp'd at
    attended_at = db.Column(db.DateTime(timezone=True))

#events
class EventTags(db.Model):
    __tablename__ = "event_tags"

    id = db.Column(db.Integer, primary_key=True)
    event_id =db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    tag =db.Column(db.String, nullable= False)

class EventEligibleZipcode(db.Model):
    __tablename__ = "event_elogible_zipcodes"

    eligible_zipcodes = db.Column(db.Integer, primary_key=True)
    event_id =db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    zipcode =db.Column(db.Integer, nullable= False)

# for contact us page
class ContactUs(db.Model):
    __tablename__ = "contact_us"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String, nullable=False)





