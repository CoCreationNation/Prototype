from datetime import datetime

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

def get_future_user_events(user_id):
    """Retrieve list of upcoming events a user has RSVP'd to."""

    now = datetime.now()
    future_events = []

    user_future_events = models.EventAttendees.query.filter(models.EventAttendees.attendee_id == user_id, models.EventAttendees.attended_at > now)

    for record in user_future_events:
        event = models.Event.query.filter(models.Event.id == record.event_id).first()
        if (event.start_utc) > now:
            future_events.append(event)
    
    return future_events