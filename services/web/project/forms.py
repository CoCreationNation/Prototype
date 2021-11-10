
"""
This file is used to initiate all forms
"""

#from Prototype.services.web.project.models import Event
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, Email, Length
from project import models 


class CreateEventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    start = DateTimeLocalField('Starting At', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end = DateTimeLocalField('Ending At', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    timezone = SelectField('US Time Zone', choices=[('US/Eastern', 'Eastern'), ('US/Central', 'Central'), ('US/Mountain', 'Mountain'), ('US/Pacific', 'Pacific')])
    restrict_attendees = BooleanField('Restrict Attendees by Zipcode')
    tags = StringField('Event Tags (comma-separtated')
    zipcodes = StringField('Zipcodes (comma-separated)')
    attendee_emails = StringField('Send invites to users (comma-seperated email addresses)')


class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label="Log In")


class RegistrationForm(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    profile_picture = FileField(label='Profile Picture')
    zip_code = StringField(label='Zip Code')
    first_name = StringField(label='First Name')
    last_name = StringField(label='Last Name')
    pronouns = SelectField(label='Pronouns', choices=[('she', 'She/Her'), 
                            ('he', 'He/Him'), ('they', 'They/Them'), 
                            ('other', 'Other')])
    address_1 = TextAreaField(label='Address')
    city = StringField(label='City')
    state = StringField(label='State')
    phone_number = StringField(label='Phone Number')

class RSVPForm(FlaskForm):
    submit = SubmitField(label='RSVP')

class DeleteUserForm(FlaskForm):
    submit = SubmitField(label='Delete User')

