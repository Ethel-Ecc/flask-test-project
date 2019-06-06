import sqlite3
import click

from flask import current_app, g
from flask.cli import with_appcontext


def db_connection():
    if 'db_config' not in g:
        g.db_config = sqlite3.connect(current_app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db_config.row_factory = sqlite3.Row

    return g.db_config


def db_close_connection(e=None):
    db_config = g.pop('db_config', None)

    if db_config is not None:
        db_config.close()


# the function below runs the sql
def initialize_db_config():
    db_connect = db_connection()

    with current_app.open_resource('strasse_store_app_schema.sql') as f:
        db_connect.executescript(f.read().decode('utf8'))

# the function below initializes the cmd when run from the terminal
@click.command('initialize-db')
@with_appcontext
def initialize_db_command():
    initialize_db_config()
    click.echo('Successfully Initialized the Database')


# the fxn below registers the db_config, terminal-initialization-cmd, and connection
# with the Application and prepares for a new initialization cmd.
# This is then imported in the AppFactory __init__.py and registered there also
def initialize_app(app):
    app.teardown_appcontext(db_close_connection)
    app.cli.add_command(initialize_db_command)

