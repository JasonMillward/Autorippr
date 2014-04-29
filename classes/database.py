"""
SQLite Database Helper


Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.5, 2013-10-20 20:40:30 CST $;
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MIT
"""

import os
from peewee import *
from datetime import datetime

database = SqliteDatabase('autoripper.sqlite', **{})

class BaseModel(Model):
    class Meta:
        database = database

class History(BaseModel):
    historyid = PrimaryKeyField(db_column='historyID')
    historydate = DateTimeField(db_column='historyDate')
    historytext = CharField(db_column='historyText')
    historytypeid = IntegerField(db_column='historyTypeID')
    movieid = IntegerField(db_column='movieID')

    class Meta:
        db_table = 'history'

class Historytypes(BaseModel):
    historytypeid = PrimaryKeyField(db_column='historyTypeID')
    historytype = CharField(db_column='historyType')

    class Meta:
        db_table = 'historyTypes'

class Movies(BaseModel):
    movieid = PrimaryKeyField(db_column='movieID')
    filename = CharField()
    path = CharField()
    filebot = BooleanField()
    statusid = IntegerField(db_column='statusID')
    lastupdated = DateTimeField(db_column='lastUpdated')

    class Meta:
        db_table = 'movies'

class Statustypes(BaseModel):
    statusid = PrimaryKeyField(db_column='statusID')
    statustext = CharField(db_column='statusText')

    class Meta:
        db_table = 'statusTypes'

def create_tables():
    database.connect()
    History.create_table()
    Historytypes.create_table()
    Movies.create_table()
    Statustypes.create_table()

def create_historyTypes():
    for hID, hType in [
            [1, 'Info'],
            [2, 'Error'],
            [3, 'MakeMKV Error'],
            [4, 'Handbrake Error']
        ]:
        Historytypes.create(historytypeid=hID, historytype=hType)

def create_statusTypes():
    for sID, sType in [
            [1, 'Added'],
            [2, 'Error'],
            [3, 'Submitted to makeMKV'],
            [4, 'Awaiting HandBrake'],
            [5, 'Submitted to HandBrake'],
            [6, 'Awaiting FileBot'],
            [7, 'Submitted to FileBot'],
            [8, 'Completed']
        ]:
        Statustypes.create(statusid=sID, statustext=sType)

def next_movie():
    for movie in Movies.select().where(Movies.statusid == 4):
        return movie


def insert_movie(*args, **kwargs):
    Movies.create(*args, **kwargs)



create_tables()
create_historyTypes()
create_statusTypes()

insert_movie(filename="test.mkv", path="/tmp/", filebot=False, statusid=1, lastupdated=datetime.now())

movie = next_movie()
print movie.path
print movie.filename
print movie.lastupdated