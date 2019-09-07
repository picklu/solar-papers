import csv
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


@app.route('/')
def home():
    name = request.args.get("name", "World")

    if name == "dsscs" or name == "prscs":
        search = False
        q = request.args.get('q')
        if q:
            search = True
        
        filepath = path.join(folder, f"{name}_papers.json")
        page = request.args.get(get_page_parameter(), type=int, default=1)
        per_page = request.args.get(get_per_page_parameter(), type=int, default=10)
        total, papers = get_json_data(filepath, page, per_page)
        pagination = Pagination(page=page, total=total, search=search, record_name='papers')
        
        return render_template('index.html',
                          papers=papers,
                          pagination=pagination,
                          )
    else:
        return f"Hello, {escape(name)}! It works."


