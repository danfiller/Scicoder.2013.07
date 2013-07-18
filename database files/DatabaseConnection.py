#!/usr/bin/python
#

import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

class Singleton(type):
	'''
	Define a singleton type.
	
	Use this singleton design pattern to be able to initialize the singleton
	the first time it's called, e.g.
	
	x = A(j=None) # the first time
	x = A()       # thereafter
	
	Otherwise, this decorater is preferred.
	http://www.python.org/dev/peps/pep-0318/#examples
	'''
	def __init__(cls, name, bases, dict):
		super(Singleton, cls).__init__(name, bases, dict)
		cls.instance = None
    
	def __call__(cls, *args, **kw):
		if cls.instance is None:
			cls.instance = super(Singleton, cls).__call__(*args, **kw)

		return cls.instance

class DatabaseConnection(object):
	'''This class defines an object that makes a connection to a database.
	   The "DatabaseConnection" object takes as its parameter the SQLAlchemy
	   database connection string.

	   This class is best called from another class that contains the
	   actual connection information (so that it can be reused for different
	   connections).
	   
	   This class implements the singleton design pattern. The first time the
	   object is created, it *requires* a valid database connection string.
	   Every time it is called via:
	   
	   db = DatabaseConnection()
	   
	   the same object is returned and contains the connection information.
	'''

	__metaclass__ = Singleton
		
	# class instance
	database_connection_string = None
	
	def __init__(self, database_connection_string=None):
		''' '''
		if database_connection_string == None:
			raise Exception("A database connection string must be provided to this class.")
		
		# Create the database engine.
		#    - change "echo" to True to print every SQL query generated
		#	 - (useful for debugging/optimization/the curious)
		self.engine = sqlalchemy.create_engine(database_connection_string, echo=False)
		
		self.Session = scoped_session(sessionmaker(bind=self.engine, autocommit=True, autoflush=True))
		self.metadata = sqlalchemy.MetaData()
		self.metadata.bind = self.engine
		self.DBClassBase = declarative_base(bind=self.engine)
	
	def close(self):
		self.engine.dispose()		


'''
Reference:
http://docs.sqlalchemy.org/en/rel_0_8/orm/session.html#sqlalchemy.orm.session.sessionmaker

autocommit = True : this prevents postgres from deadlocking on long-lived session processes (e.g. a background daemon), that produces 'idle in transaction' processes in PostgreSQL.
autoflush = False: prevents flushing (i.e. commiting) objects when only performing a SELECT statement, i.e. when not modifying the db

Sample code to account for different cases (if things change for whatever reason):

if session.autocommit:
	session.begin()
<do stuff>
session.commit()

Try to minimise the work done in between session.begin() and session.commit().
'''
