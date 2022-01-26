from flask_sqlalchemy import SQLAlchemy


## Define DB object
db = SQLAlchemy()

def init_app(app):
    db.init_app(app)
    db.create_all(app=app)
