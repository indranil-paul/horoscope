import os


class Config(object):
    ## API version
    VERSION = 'v1'

    ## HOST & PORT
    HOST = '0.0.0.0'
    PORT = 8088

    ## Statement for enabling the development environment
    DEBUG = True

    ## Define the application directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    ## Define Database we are working with. 
    ## Database: SQLite
    DBFILE_NAME = 'app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ## Application threads
    THREADS_PER_PAGE = 2

    ## Enable protection against *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = 'secret'

    ## Secret key for signing cookies
    SECRET_KEY = 'secret'


class ProductionConfig(Config):
    PORT = 8182
    ENV = 'production'
    DEBUG = False
    DATABASE_CONNECTION_OPTIONS = {}
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(Config.BASE_DIR, Config.DBFILE_NAME)    # Syntax is specific for SQLite


class DevelopmentConfig(Config):
    ENV = 'development'
    DEVELOPMENT = True
    DEBUG = True
    DATABASE_CONNECTION_OPTIONS = {}
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(Config.BASE_DIR, Config.DBFILE_NAME)    # Syntax is specific for SQLite
