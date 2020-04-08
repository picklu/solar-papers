import sqlite3
from config import DATABASE, SCHEMA
from flask import g

INSERT = 'INSERT INTO papers (PaperNumber, PageNumber) VALUES(?, ?);'
FETCH = 'SELECT * FROM papers;'
FETCH_ONE = 'SELECT * FROM papers ORDER BY Id DESC LIMIT 1;'


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = make_dicts
    return db

def insert_papers(app, args, many=False):
    with app.app_context():
        conn = get_db()
        cursor = conn.cursor()
        if many:
            cursor.executemany(INSERT, args)
        else:
            cursor.execute(INSERT, args)
        conn.commit()
        total_changes = conn.total_changes
        conn.close()
        return total_changes

def get_papers(app, all=False):
    with app.app_context():
        conn = get_db()
        cursor = conn.cursor()
        if all:
            cursor.execute(FETCH)
            data = cursor.fetchall()
        else:
            cursor.execute(FETCH_ONE)
            data = cursor.fetchone()
        conn.close()
        return data

def init_db(app):
    with app.app_context():
        db = get_db()
        with app.open_resource(SCHEMA, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()