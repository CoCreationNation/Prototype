from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.fields.html5 import DateField, TimeField, DateTimeLocalField
from wtforms.validators import DataRequired

class CreateEventForm(FlaskForm):
    title = StringField('Title')
    description = TextAreaField('Description')
    start = DateTimeLocalField('Starting At', format='%Y-%m-%dT%H:%M')
    end = DateTimeLocalField('Ending At', format='%Y-%m-%dT%H:%M')