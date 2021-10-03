
"""
This file is used to initiate all forms
"""

#from Prototype.services.web.project.models import Event
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, Email, Length


class CreateEventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    start = DateTimeLocalField('Starting At', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end = DateTimeLocalField('Ending At', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    restrict_attendees = BooleanField('Restrict Attendees by Zipcode')
    tags = StringField('Event Tags (comma-separtated')
    zipcodes = StringField('Zipcodes (comma-separated)')
    attendee_emails = StringField('Send invites to users (comma-seperated email addresses)')
    
    

class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(label="Log In")


class RegistrationForm(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    zip_code = StringField(label='Zip Code')
