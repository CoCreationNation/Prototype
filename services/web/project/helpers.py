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

def save_event_to_user(event, user):
    """Saves event to user when they RSVP."""

    user.events.append(event)
    db.session.add(user)
    db.session.commit()

    return user.events



