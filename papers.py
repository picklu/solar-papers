from flask import Flask, escape, g, json, request, render_template
from flask_paginate import Pagination, get_page_parameter, get_per_page_parameter
from config import DATA, JSON_PATH
from db import insert_papers, get_papers


app = Flask(__name__)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


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
    page_number = get_papers(app).get("PageNumber", 1)
    page = request.args.get(get_page_parameter(), type=int, default=page_number)
    per_page = request.args.get(get_per_page_parameter(), type=int, default=20)
    total, papers = get_json_data(JSON_PATH, page, per_page)
    pagination = Pagination(page=page, per_page=per_page, 
                            total=total, search=search, 
                            record_name='papers', css_framework='bootstrap4')
    
    return render_template('index.html', fixed="", solar=solar,
                            papers=papers, pagination=pagination)


@app.route('/status')
def status():
    data = get_papers(app, True)
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


# 404 error
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


