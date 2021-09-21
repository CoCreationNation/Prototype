from datetime import datetime

from project import models

def get_future_events() -> list:
    now = datetime.now()
    future_events = models.Event.query.filter(models.Event.end_utc > now).all()
    return future_events

def get_user_info(user_id):
    """Retrieve user using id"""
    
    return models.User.query.get(user_id)

