
"""
This file is used to initiate all forms
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField
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

class RSVPForm(FlaskForm):
    submit = SubmitField(label='RSVP')