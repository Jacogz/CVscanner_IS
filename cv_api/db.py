from flask import Flask, current_app, g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import click

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

@click.command('init_db')
@with_appcontext
def init_db_command():
    from .src.models import documento, usuario
    db.create_all()
    click.echo('DB Inicializada')

def init_app(app):
    db.init_app(app)
    app.cli.add_command(init_db_command)
    