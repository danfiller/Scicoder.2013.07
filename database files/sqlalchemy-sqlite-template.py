#!/usr/bin/python

import os, sys
import sqlalchemy
from sqlalchemy import MetaData, ForeignKey, create_engine
from sqlalchemy import Table, Column, Integer, Float, String, Numeric, Boolean
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import between

# enter the database name here
db_filename = "xxx.sqlite"

# --------------------------------------------------------
# Set up the database connection - no modification needed
# --------------------------------------------------------
db_connection_string = "sqlite:///%s" % db_filename
engine = create_engine(db_connection_string, echo=False)
metadata = MetaData()
metadata.bind = engine
Base = declarative_base()
# --------------------------------------------------------

# ================================================
# == Define model classes ==
# ==========================
class ...(Base):
	__tablename__ = ""

	'''Update with your own tables'''
	id = Column(Integer, primary_key=True)
	ra = Column(Float, index=True)
	dec = Column(Float, index=True)
	line = Column(String)

# generate tables in db
Base.metadata.create_all(engine)
# ================================================

# create session
Session = scoped_session(sessionmaker(bind=engine, autocommit=True, autoflush=False))
session = Session()

session.begin()

# ... your code here ...

session.commit()

sys.exit(0)