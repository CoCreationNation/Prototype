"""
This file contains all the database models for the Flask app.
"""
from sqlalchemy import sql

from project import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, email):
        self.email = email


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
