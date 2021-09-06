"""
This file contains all the database models for the Flask app.
"""
from project import db

#for pronouns
import enum 

class Pronouns(enum.Enum): 
    she = "She/Her"
    he = "He/Him"
    they = "They/Them"
    other = "Other"

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, 
                    primary_key=True,
                    autoincrement=True,
                    nullable=False)
    password_hash = db.Column(db.String, unique=True, nullable=False) #need to incorporate password_hash algo somehow
    user_type = db.Column(db.String)
    is_superuser = db.Column(db.Boolean()) #how are we defining this? do we want a default value?
    last_name = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    pronouns = db.Column(db.Enum(Pronouns))
    email = db.Column(db.String(128), unique=True, nullable=False)
    email_confirmed = db.Column(db.Boolean(), default=True)
    address_1 = db.Column(db.String, nullable=False) #should any of these address fields should be nullable=False?
    address_2 = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zipcode = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime)
    
    #did is_superuser replace the active field? can we delete this?
    active = db.Column(db.Boolean(), default=True, nullable=False) 

    def __init__(self, email):
        self.email = email

    #added a __repr__ to help visualize the User object
    def __repr__(self):
        return f'<User id={self.id} email={self.email}>'    
