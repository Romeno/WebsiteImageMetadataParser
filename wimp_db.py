# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, String, Text, TIMESTAMP,text, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


# class UrlEntry(Base):
# 	pass


engine = None
DBSession = None
session = None


def connect(db_username, db_password, db_host, db_name):
	global engine
	global DBSession
	global session

	engine = create_engine('postgresql://{}:{}@{}/{}'.format(db_username, db_password, db_host, db_name))

	Base.metadata.bind = engine

	DBSession = sessionmaker(bind=engine)

	session = DBSession()


def create_db():
	Base.metadata.create_all(engine)


def get_url_entries():
	return [1]
	# return session.query(UrlEntry).all()


def store_to_db(image_metadata):
	imm = None

	# session.add(imm)
	# session.commit()
