"""
This file contains all the database models for the Flask app.
"""
from project import db
from project import app
from flask_login import UserMixin, LoginManager

# for pronouns
import enum


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class Pronouns(enum.Enum):
    she = "She/Her"
    he = "He/Him"
    they = "They/Them"
    other = "Other"


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)  # need to incorporate password_hash algo somehow
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







    # added a __repr__ to help visualize the User object

