"""
SQLite Database Helper


Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.6.1, 2014-08-18 10:42:00 CST $;
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MIT
"""

import os
from peewee import *
from datetime import datetime

database = SqliteDatabase('autorippr.sqlite', **{})


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
    moviename = CharField()
    path = CharField()
    filename = CharField(null=True)
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


def create_history_types():
    historyTypes = [
        [1, 'Info'],
        [2, 'Error'],
        [3, 'MakeMKV Error'],
        [4, 'Handbrake Error']
    ]

    c = 0
    for z in Historytypes.select():
        c += 1

    if c != len(historyTypes):
        for hID, hType in historyTypes:
            Historytypes.create(historytypeid=hID, historytype=hType)


def create_status_types():
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

    if c != len(statusTypes):
        for sID, sType in statusTypes:
            Statustypes.create(statusid=sID, statustext=sType)


def next_movie_to_compress():
    for movie in Movies.select().where((Movies.statusid == 4) & (Movies.filename != "None")):
        return movie


def next_movie_to_filebot():
    for movie in Movies.select().where((Movies.statusid == 6) & (Movies.filename != "None") & (Movies.filebot == 1)):
        return movie


def insert_history(dbMovie, text, typeid=1):
    return History.create(
        movieid=dbMovie.movieid,
        historytext=text,
        historydate=datetime.now(),
        historytypeid=typeid
    )


def insert_movie(title, path, filebot):
    return Movies.create(
        moviename=title,
        path=path,
        filename="None",
        filebot=filebot,
        statusid=1,
        lastupdated=datetime.now()
    )


def update_movie(movieOBJ, statusid, filename=None):
    movieOBJ.statusid = statusid
    movieOBJ.lastupdated = datetime.now()

    if filename is not None:
        movieOBJ.filename = filename

    movieOBJ.save()


def db_integrity_check():
    # Stuff
    create_tables()

    # Things
    create_history_types()
    create_status_types()

db_integrity_check()
