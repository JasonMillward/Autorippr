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

    # Fail silently if tables exists
    History.create_table(True)
    Historytypes.create_table(True)
    Movies.create_table(True)
    Statustypes.create_table(True)

def create_historyTypes():
    historyTypes = [
        [1, 'Info'],
        [2, 'Error'],
        [3, 'MakeMKV Error'],
        [4, 'Handbrake Error']
    ]

    c = 0
    for z in Historytypes.select():
        c += 1

    if c != len( historyTypes ):
        for hID, hType in historyTypes:
            Historytypes.create(historytypeid=hID, historytype=hType)

def create_statusTypes():
    statusTypes = [
        [1, 'Added'],
        [2, 'Error'],
        [3, 'Submitted to makeMKV'],
        [4, 'Awaiting HandBrake'],
        [5, 'Submitted to HandBrake'],
        [6, 'Awaiting FileBot'],
        [7, 'Submitted to FileBot'],
        [8, 'Completed']
    ]

    c = 0
    for z in Statustypes.select():
        c += 1

    if c != len( statusTypes ):
        for sID, sType in statusTypes:
            Statustypes.create(statusid=sID, statustext=sType)

def next_movie():
    for movie in Movies.select().where(Movies.statusid == 4):
        return movie

def insert_history(id, text):
    return History.create(
        movieid=id,
        historytext=text,
        historydate=datetime.now(),
        historytypeid=1
    )

def insert_movie(title, path, filebot):
    return Movies.create(
        filename=title,
        path=path,
        filebot=filebot,
        statusid=1,
        lastupdated=datetime.now()
    )

def update_movie(movieOBJ, statusid):
    movieOBJ.statusid = statusid
    movieOBJ.lastupdated = datetime.now()
    movieOBJ.save()

def dbintegritycheck():
    # Stuff
    create_tables()

    # Things
    create_historyTypes()
    create_statusTypes()

dbintegritycheck()