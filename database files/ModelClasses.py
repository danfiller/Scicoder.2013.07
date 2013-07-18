#!/usr/bin/python

from DatabaseConnection import DatabaseConnection

import sqlalchemy
from sqlalchemy.orm import relation
from sqlalchemy.ext.declarative import declarative_base

dbc = DatabaseConnection()

# ========================
# Define database classes
# ========================
Base = declarative_base(bind=dbc.engine)

class Student(Base):
	__tablename__ = 'student'
	__table_args__ = {'autoload' : True}

class Status(Base):
	__tablename__ = 'status'
	__table_args__ = {'autoload' : True}

class Club(Base):
	__tablename__ = 'club'
	__table_args__ = {'autoload' : True}

class StudentToClub(Base):
	__tablename__ = 'student_to_club'
	__table_args__ = {'autoload' : True}

class Supervisor(Base):
	__tablename__ = 'supervisor'
	__table_args__ = {'autoload' : True}

class StudentToSupervisor(Base):
	__tablename__ = 'student_to_supervisor'
	__table_args__ = {'autoload' : True}

# =========================
# Define relationships here
# =========================

Student.clubs = relation(Club,
						 secondary=StudentToClub.__table__, # the join table
						 primaryjoin=Student.id==StudentToClub.student_id,
						 secondaryjoin=StudentToClub.club_id==Club.id, # note that this is the Table, not the object class!
						 foreign_keys=[StudentToClub.student_id,StudentToClub.club_id],
						 backref="students")

Student.status = relation(Status,
						  primaryjoin=Student.status_id==Status.id,
						  foreign_keys=[Student.status_id],
						  backref="students")

Student.supervisors = relation(Supervisor,
							   secondary=StudentToSupervisor.__table__,
							   primaryjoin=Student.id==StudentToSupervisor.student_id,
							   secondaryjoin=StudentToSupervisor.supervisor_id==Supervisor.id,
							   foreign_keys=[StudentToSupervisor.student_id, StudentToSupervisor.supervisor_id],
							   backref="students")




