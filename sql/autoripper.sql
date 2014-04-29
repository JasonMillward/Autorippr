DROP TABLE IF EXISTS "history";
CREATE TABLE "history" (
    "historyID" INTEGER PRIMARY KEY  NOT NULL ,
    "movieID" INTEGER NOT NULL ,
    "historyTypeID" INTEGER NOT NULL  DEFAULT (null) REFERENCES historyTypes(historyTypes_historyTypeID),
    "historyDate" DATETIME NOT NULL  DEFAULT (CURRENT_TIMESTAMP) ,
    "historyText" VARCHAR NOT NULL
);

DROP TABLE IF EXISTS "historyTypes";
CREATE TABLE "historyTypes" (
    "historyTypeID" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL ,
    "historyType" VARCHAR NOT NULL  UNIQUE
);

DROP TABLE IF EXISTS "movies";
CREATE TABLE "movies" (
    "movieID" INTEGER PRIMARY KEY NOT NULL ,
    "file" VARCHAR NOT NULL  DEFAULT (null) ,
    "path" VARCHAR NOT NULL  DEFAULT (null) ,
    "filebot" BOOL NOT NULL ,
    "statusID" INTEGER NOT NULL REFERENCES statusTypes(statusTypes_statusID)  ,
    "lastUpdated" DATETIME NOT NULL
);

DROP TABLE IF EXISTS "statusTypes";
CREATE TABLE "statusTypes" (
    "statusID" INTEGER PRIMARY KEY  NOT NULL ,
    "statusText" VARCHAR NOT NULL  DEFAULT (null)
);

INSERT INTO "historyTypes" VALUES(1,'Info');
INSERT INTO "historyTypes" VALUES(2,'Error');
INSERT INTO "historyTypes" VALUES(3,'MakeMKV Error');
INSERT INTO "historyTypes" VALUES(4,'Handbrake Error');

INSERT INTO "statusTypes" VALUES(1,'Added');
INSERT INTO "statusTypes" VALUES(2,'Error');
INSERT INTO "statusTypes" VALUES(3,'Submitted to makeMKV');
INSERT INTO "statusTypes" VALUES(4,'Submitted to handbrake');
INSERT INTO "statusTypes" VALUES(5,'Submitted to FileBot');
INSERT INTO "statusTypes" VALUES(6,'Completed');
