from datetime import datetime, timedelta

from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash

from project import app, db, models

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    print('Seeding DB...')
    event1 = models.Event(
        start_utc = datetime.now() + timedelta(days=2),
        end_utc = datetime.now() + timedelta(days=2) + timedelta(hours=2),
        title = 'My First Event',
        image_url = 'event1.jpeg',
        description = 'This event will be so much fun because it is my first event and there will be many exciting things to do.'
    )
    db.session.add(event1)
    
    event2 = models.Event(
        start_utc = datetime.now() + timedelta(days=3),
        end_utc = datetime.now() + timedelta(days=3) + timedelta(hours=2),
        title = 'My Second Event',
        image_url = 'event2.jpeg',
        description = 'In this meeting we will be discussing the finer points of Web Development using a python. The snake, not the language.'
    )
    db.session.add(event2)

    event3 = models.Event(
        start_utc = datetime.now() - timedelta(minutes=3),
        end_utc = datetime.now() + timedelta(hours=2),
        title = 'My Live Event',
        image_url = 'event3.jpeg',
        description = 'This is the Event where we see all our lovely faces.'
    )
    db.session.add(event3)

    event4 = models.Event(
        start_utc = datetime.now() + timedelta(days=1),
        end_utc = datetime.now() + timedelta(days=1) + timedelta(hours=2),
        title = 'Event the Fourth',
        image_url = 'event3.jpeg',
        description = 'In this meeting we will be discussing the finer points of Web Development using a python. The snake, not the language.'
    )
    db.session.add(event4)

    event5 = models.Event(
        start_utc = datetime.now() + timedelta(days=3),
        end_utc = datetime.now() + timedelta(days=3) + timedelta(hours=2),
        title = 'Event 5 rocks!',
        image_url = 'event3.jpeg',
        description = 'In this meeting we will be discussing the finer points of Web Development using a python. The snake, not the language.'
    )
    db.session.add(event5)

    event6 = models.Event(
        start_utc = datetime.now() + timedelta(days=5),
        end_utc = datetime.now() + timedelta(days=5) + timedelta(hours=2),
        title = '6 Event',
        image_url = 'event3.jpeg',
        description = 'In this meeting we will be discussing the finer points of Web Development using a python. The snake, not the language.'
    )
    db.session.add(event6)

    event7 = models.Event(
        start_utc = datetime.now() + timedelta(days=7),
        end_utc = datetime.now() + timedelta(days=7) + timedelta(hours=2),
        title = 'Seven Whole Events',
        image_url = 'event3.jpeg',
        description = 'Yee haw!'
    )
    db.session.add(event7)

    event8 = models.Event(
        start_utc = datetime.now() + timedelta(days=12),
        end_utc = datetime.now() + timedelta(days=12) + timedelta(hours=2),
        title = 'My eighth Event',
        image_url = 'event3.jpeg',
        description = 'Its crazy Eights'
    )
    db.session.add(event8)

    db.session.commit()

    admin1_password = generate_password_hash(
            'secret',
            method='pbkdf2:sha256',
            salt_length=8
        )
    admin1 = models.User(
        username="admin1",
        password=admin1_password,
        email="admin1@example.com",
        zip_code='90064',
        user_type='admin'
    )
    db.session.add(admin1)

    user1_password = generate_password_hash(
            'secret1',
            method='pbkdf2:sha256',
            salt_length=8
        )
    user1 = models.User(
        username="a_user",
        password=user1_password,
        email="a_user@example.com",
        zip_code='90064'
    )
    db.session.add(user1)

    user2_password = generate_password_hash(
            'secret2',
            method='pbkdf2:sha256',
            salt_length=8
        )
    user2 = models.User(
        username="another_user",
        password=user2_password,
        email="another_user@example.com",
        zip_code='90064'
    )
    db.session.add(user2)

    user3_password = generate_password_hash(
            'secret3',
            method='pbkdf2:sha256',
            salt_length=8
        )
    user3 = models.User(
        username="not_another_user",
        password=user3_password,
        email="not_another_user@example.com",
        zip_code='90065'
    )
    db.session.add(user3)

    db.session.commit()

    attendee1 = models.EventAttendees(
        event_id=1,
        attendee_id=2
    )
    db.session.add(attendee1)

    attendee2 = models.EventAttendees(
        event_id=2,
        attendee_id=2
    )
    db.session.add(attendee2)

    attendee3 = models.EventAttendees(
        event_id=3,
        attendee_id=2
    )
    db.session.add(attendee3)

    attendee4 = models.EventAttendees(
        event_id=4,
        attendee_id=2
    )
    db.session.add(attendee4)


    db.session.commit()


if __name__ == "__main__":
    cli()