import sqlite3
from os import path
from flask import Flask, escape, g, json, request, render_template
from flask_paginate import Pagination, get_page_parameter, get_per_page_parameter


app = Flask(__name__)

DATA = path.join(path.dirname(__file__), "data")
DATABASE = path.join(DATA, 'database.db')
SCHEMA = path.join(DATA, 'schema.sql')
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

def insert_paper(args):
    with app.app_context():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(INSERT, args)
        conn.commit()
        total_changes = conn.total_changes
        conn.close()
        return total_changes

def get_papers(all=False):
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



@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource(SCHEMA, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_json_data(filename, page, per_page):
    with open(filename) as infile:
        data = json.load(infile)["data"]
        start = (page - 1) * per_page
        end = start + per_page
        return [len(data), data[start : end]]


# index 
@app.route('/')
def index(solar=""):
    search = False
    q = request.args.get('q')
    if q:
        search = True
    
    filepath = path.join(DATA, "papers.json")
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = request.args.get(get_per_page_parameter(), type=int, default=20)
    total, papers = get_json_data(filepath, page, per_page)
    pagination = Pagination(page=page, per_page=per_page, 
                            total=total, search=search, 
                            record_name='papers', css_framework='bootstrap4')
    
    return render_template('index.html', fixed="", solar=solar,
                            papers=papers, pagination=pagination)


# 404 error
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


