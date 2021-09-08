"""
This file contains all the database models for the Flask app.
"""
from sqlalchemy import sql

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
    is_superuser = db.Column(db.Boolean(), default=False)
    last_name = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    pronouns = db.Column(db.Enum(Pronouns))
    email = db.Column(db.String(128), unique=True, nullable=False)
    email_confirmed = db.Column(db.Boolean(), default=False)
    address_1 = db.Column(db.String)
    address_2 = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zipcode = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<User id={self.id} email={self.email}>'  


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    start_utc = db.Column(db.DateTime(timezone=True), nullable=False)
    end_utc = db.Column(db.DateTime(timezone=True), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=sql.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=sql.func.now(), nullable=True)
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)
