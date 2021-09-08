from datetime import datetime, time, timedelta

from flask.cli import FlaskGroup

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
    db.session.commit()


if __name__ == "__main__":
    cli()