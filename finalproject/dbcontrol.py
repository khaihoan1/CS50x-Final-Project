import sqlite3
from .models import db
import click
from flask import current_app, g
from flask.cli import with_appcontext

# def get_db():
#     if 'database' not in g:
#         g.database = sqlite3.connect(
#             current_app.config['DATABASE'],
#             detect_types=sqlite3.PARSE_DECLTYPES
#         )
#         g.db.row_factory = sqlite3.Row
    
#     return g.db

# def close_db(e=None):
#     database = g.pop('database', None)

#     if database is not None:
#         database.close()

def init_db():
    db.create_all()
    # migrate.init_app(current_app, db)
    # with current_app.open_resource('schema.sql') as f:
    #     db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    # app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)



# @click.command(name="create")
# @with_appcontext
# def create():
#     db.create_all()

# app.cli.add_command(create)