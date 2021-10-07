
"""
This file is used to initiate all forms
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, SelectField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, Email, Length
from project import models 


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
    first_name = StringField(label='First Name')
    last_name = StringField(label='Last Name')
    pronouns = SelectField(label='Pronouns', choices=[('she', 'She/Her'), 
                            ('he', 'He/Him'), ('they', 'They/Them'), 
                            ('other', 'Other')])
    address_1 = TextAreaField(label='Address')
    city = StringField(label='City')
    state = StringField(label='State')
    phone_number = StringField(label='Phone Number')

