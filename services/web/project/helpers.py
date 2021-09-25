from datetime import datetime

from project import models

def get_future_events() -> list:
    now = datetime.now()
    future_events = models.Event.query.filter(models.Event.end_utc > now).all()
    return future_events

def get_user_info(user_id):
    """Retrieve user using id"""
    
    return models.User.query.get(user_id)

def get_past_events() -> list:
    now = datetime.now()
    past_events = models.Event.query.filter(models.Event.end_utc < now).all()
    return past_events

def get_user_events(user_id):
    """Retrieve the events a user has attended"""
    
    get_past_events

    #if a user_id == attendee_id in any of these events
    #OR is a user already connected to the events they've RSVPed to in models.py?
    #return user_events


