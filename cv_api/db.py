from sqlalchemy import create_engine
from

# Make database connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

# Close database connection
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# Initialize database executing schema.sql
def init_db():
    db = get_db()
    
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# Command line interface to initialize database
@click.command('init-db')
def init_db_command(): 
    init_db()
    click.echo('Initialized the database.')

# Timestamp converter for SQLite (Interpret as datetime)
sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

# Register functions with flask app
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)