from os import path
from flask import Flask, escape, json, request, render_template
from flask_paginate import Pagination, get_page_parameter, get_per_page_parameter


app = Flask(__name__)

folder = path.join(path.dirname(__file__), "data")

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
    
    filepath = path.join(folder, "papers.json")
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


