#!/usr/bin/python

import sqlalchemy
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine import Engine
from DatabaseConnection import DatabaseConnection

# Fill in database connection information here.
sqlite_db = {
	'name'	: 'testdb.sqlite' # this is the name of the file
}

# ===================================================================
# Below is template code that you probably don't need to modify.
# ===================================================================

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
	'''
	This ensures that the foreign key support is enabled when connecting to db.
	
	SQLite supports foreign keys if:
		- sqlite3 version >= 3.6.19
		- compiled without SQLITE_OMIT_FOREIGN_KEY or SQLITE_OMIT_TRIGGER flags
		- foreign key support is explicity enabled upon db connection
		
	Ref: http://sqlite.org/foreignkeys.html#fk_enable
	'''
	cursor = dbapi_connection.cursor()
	cursor.execute("PRAGMA foreign_keys=ON")
	cursor.close()

# For more options of SQLite connection strings, see:
# http://www.sqlalchemy.org/docs/reference/dialects/sqlite.html#connect-strings

db_connection_string = "sqlite:///%s" % sqlite_db['name']

# This allows the file to be 'import'ed any number of times, but attempts to
# connect to the database only once.
try:
	database = DatabaseConnection() # fails if connection not yet made.
except:
	database = DatabaseConnection(database_connection_string=db_connection_string)

engine = database.engine
metadata = database.metadata
#Session = sessionmaker(bind=engine, autocommit=True, autoflush=False)
Session = scoped_session(sessionmaker(bind=engine, autocommit=True, autoflush=False))

