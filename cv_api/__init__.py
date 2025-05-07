import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLAlchemy_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'cv_api.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Initialize the database using db.py
    from . import db
    db.init_app(app)
    
    # Register blueprints
    from .src.blueprints import auth, docs
    app.register_blueprint(auth.bp)
    app.register_blueprint(docs.bp)
    

    return app