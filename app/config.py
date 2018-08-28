import os


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'jnw639kO3{28W1cvtDl]tjdrzkkd3YJCB(2IPK1deBKe*v!I6e0NB1$n3admTreE79Q%MxOuVtVFbuAsb69Mb2gPPpCQ?GAFcUMoH'
    TOKEN_VALIDITY = 180
    username = os.environ.get('MYSQL_USERNAME')
    password = os.environ.get('MYSQL_PASSWORD')
    hostname = os.environ.get('MYSQL_HOSTNAME')
    port = os.environ.get('MYSQL_PORT')
    database = os.environ.get('MYSQL_DATABASE')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}?charset=utf8mb4'

    ENABLE_MAIL = True

    SMTP_HOSTNAME = os.environ.get('SMTP_HOSTNAME')
    SMTP_PORT = os.environ.get('SMTP_PORT')
    SMTP_USERNAME = os.environ.get('SMTP_USERNAME')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')

    # TODO add something
    MAIL_SUBJECT = "Subject"
    MAIL_MESSAGE = "Message"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:9999/hc?charset=utf8mb4'
    DB_CHARSET = 'utf8'


class DevelopmentConfig(Config):
    ENABLE_MAIL = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:9999/hc?charset=utf8mb4'
    DB_CHARSET = 'utf8'


class TestingConfig(Config):
    ENABLE_MAIL = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True