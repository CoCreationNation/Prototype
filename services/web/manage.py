from datetime import datetime, time, timedelta

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
        description = 'This event will be so much fun because it is my first event and there will be many exciting things to do.'
    )
    db.session.add(event1)
    
    event2 = models.Event(
        start_utc = datetime.now() + timedelta(days=3),
        end_utc = datetime.now() + timedelta(days=3) + timedelta(hours=2),
        title = 'My Second Event',
        description = 'In this meeting we will be discussing the finer points of Web Development using a python. The snake, not the language.'
    )
    db.session.add(event2)

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


if __name__ == "__main__":
    cli()