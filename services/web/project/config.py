import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    ENVIRONMENT = os.getenv("ENVIRONMENT")
    if ENVIRONMENT == 'prod':
        host = os.getenv('RDS_HOST')
        username = os.getenv('RDS_MASTER_USER')
        password = os.getenv('RDS_MASTER_PASSWORD')
        SQLALCHEMY_DATABASE_URI = f'postgresql://{username}:{password}@{host}:5432/postgres'
    else:
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SECRET_KEY = os.urandom(12)
    SECRET_KEY = 'bar-apple'
    SECURITY_PASSWORD_SALT = 'foo-banana'

    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = os.environ['APP_MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']

    # mail accounts
    MAIL_DEFAULT_SENDER = 'cocreation.nation.dev@gmail.com'