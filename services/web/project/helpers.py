from datetime import datetime

from project import models, db

def get_future_events() -> list:
    now = datetime.now()
    future_events = models.Event.query.filter(models.Event.end_utc > now).all()
    return future_events

def get_user_info(user_id):
    """Retrieve user using id"""
   
    return models.User.query.get(user_id)

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

