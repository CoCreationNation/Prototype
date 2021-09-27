
"""
This file is used to initiate all forms
"""

#from Prototype.services.web.project.models import Event
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, Email, Length


class CreateEventForm(FlaskForm):
    title = StringField('Title')
    description = TextAreaField('Description')
    start = DateTimeLocalField('Starting At', format='%Y-%m-%dT%H:%M')
    end = DateTimeLocalField('Ending At', format='%Y-%m-%dT%H:%M')


class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(label="Log In")


class RegistrationForm(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    zip_code = StringField(label='Zip Code')

class UserEventForm(FlaskForm):
    id = IntegerField('ID')
    event_id = IntegerField('Event ID', validators=[DataRequired()])
    attendee_id = IntegerField('Attendeee ID', validators=[DataRequired()])
    attended_at= BooleanField('Attended')
    zipcode=IntegerField('Zipcode', validators=[DataRequired()])

class EventAdminForm(FlaskForm):
    id = IntegerField('ID')
    user_id = IntegerField('User ID', validators=[DataRequired()])
    event_id = IntegerField('Event ID', validators=[DataRequired()])
    #rsvp_at = StringField('Email for RSVP',validators=[DataRequired()]) 
    admin_level = StringField('Admin Level')

