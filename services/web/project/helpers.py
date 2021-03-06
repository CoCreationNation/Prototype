from datetime import datetime
import os
from typing import Optional


from twilio.rest import Client

import pytz

from project import models, db

def get_future_events() -> list:
    now = datetime.now()
    future_events = models.Event.query.filter(models.Event.end_utc > now).all()
    return future_events



def get_user_info(user_id):
    """Retrieve user using id"""
   
    return models.User.query.get(user_id)

def get_event_by_id(event_id):
    """Return an event by primary key/id."""

    return models.Event.query.get(event_id)

def get_event_time(event_id):
    """Return the start time of an event by id."""
    event = models.Event.query.get(event_id)

    return event.start_utc

def get_user_events(user_id): 
    """Retrieve the events a user has attended"""
    
    #identify all records in event_attendees 1) that are attached to user and 2) where the user actually attended
    user_attendee_records = models.EventAttendees.query.filter(models.EventAttendees.attendee_id == user_id, 
                                                                models.EventAttendees.attended_at != None).all()
    user_past_events = set()
    now = datetime.now()

    #isolate the event records using the ids from event_attendees AND where event has already passed
    for record in user_attendee_records: 
        event = models.Event.query.filter(models.Event.id == record.event_id).first()
        #now make sure the event has already passed 
        if (event.end_utc < now): 
            user_past_events.add(event)

    #TODO: order events by date
    return user_past_events

def update_user_details(user_id, first_name, last_name, pronouns, address_1, city, state, zip_code, phone_number): 
    """Update a user's details"""

    user = get_user_info(user_id)
    
    if zip_code: #zip_code is not a nullable field in models.py
        
        zip_code = int(float(zip_code))

        models.User.query.filter(models.User.id == user_id).update(
            {
                "first_name": first_name,
                "last_name": last_name,
                "pronouns": pronouns,
                "address_1": address_1,
                "city": city,
                "state": state,
                "zip_code": zip_code,
                "phone_number": phone_number
            }
        )
    else:
        models.User.query.filter(models.User.id == user_id).update(
            {
                "first_name": first_name,
                "last_name": last_name,
                "pronouns": pronouns,
                "address_1": address_1,
                "city": city,
                "state": state,
                "phone_number": phone_number
            }
        )

    
    db.session.commit() 

    return user

def get_chatroom(name):
    twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    twilio_api_key_sid = os.environ.get('TWILIO_API_KEY_SID')
    twilio_api_key_secret = os.environ.get('TWILIO_API_KEY_SECRET')
    twilio_client = Client(twilio_api_key_sid, twilio_api_key_secret,
                       twilio_account_sid)
    for conversation in twilio_client.conversations.conversations.stream():
        if conversation.friendly_name == name:
            return conversation

    # a conversation with the given name does not exist ==> create a new one
    return twilio_client.conversations.conversations.create(
        friendly_name=name)

def get_future_user_events(user_id: int) -> list:
    """Retrieve list of upcoming events a user has RSVP'd to."""

    now = datetime.now()
    future_events = []

    user_events = models.EventAttendees.query.filter(models.EventAttendees.attendee_id == user_id)

    for record in user_events:
        event = models.Event.query.filter(models.Event.id == record.event_id).first()
        print(f'start type: {type(event.start_utc)}')
        if (event.start_utc.replace(tzinfo=None)) > now:
            future_events.append(event)
    
    return future_events


def convert_dateime_to_utc(dt: datetime, tz: str) -> datetime:
    local = pytz.timezone(tz)
    naive = dt
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt


def group_list_by_threes(items: list, new_list: Optional[list] = None) -> list:
    """
    This function takes a list of items and groups it into a list of lists, with
    three items in each inner list.
    """
    new_list = [] if not new_list else new_list

    new_list.append(items[:3])
    new_items = items[3:]
    if new_items:
        group_list_by_threes(new_items, new_list)
    
    return new_list


def delete_user(user_id):
    """Delete a user by id."""

    return models.User.query.filter_by(id = user_id).delete()
    

