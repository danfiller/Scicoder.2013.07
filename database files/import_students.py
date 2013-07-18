#!/usr/bin/env python

import sys
import sqlalchemy
from SQLiteConnection import engine, Session
from ModelClasses import *


filename = 'student_data.txt'
data = open(filename)

session = Session()
session.begin()

line = data.readline()
while line[0] == '#':
	line = data.readline()

keys = line.rstrip().split('|')

i = 0
for line in data:
	i += 1
	vals = line.rstrip().split('|')
	entry = dict(zip(keys,vals))
	
	current_student = Student()
	current_student.first_name = entry['first_name']
	current_student.last_name = entry['last_name']
	session.add(current_student)
	
	try:
	   student_status = session.query(Status) \
				.filter(Status.label==entry['status']).one()
	except sqlalchemy.orm.exc.NoResultFound:
		student_status = Status()
		student_status.label=entry['status']
		session.add(student_status)
	
	current_student.status = student_status

	if entry['supervisors'] != '':
		super_list = entry['supervisors'].split(', ')
		for supinfo in super_list:
			sup = supinfo.split('/')
		
			try:
				one_super = session.query(Supervisor) \
				   .filter(Supervisor.name==sup[0]).one()
			except sqlalchemy.orm.exc.NoResultFound:
				one_super = Supervisor()
				one_super.name = sup[0]
				one_super.room = sup[1]
				session.add(one_super)
			current_student.supervisors.append(one_super)


	if 'club' in entry and entry['club'] != '':
		club_list = entry['club'].split(', ')
		for club_name in club_list:
			try:
				one_club = session.query(Club) \
				   .filter(Club.name==club_name).one()
			except sqlalchemy.orm.exc.NoResultFound:
				one_club = Club()
				one_club.name = club_name.strip()
				session.add(one_club)

			current_student.clubs.append(one_club)

data.close()

session.commit()

engine.dispose() # cleanly disconnect from the database
sys.exit(0)
