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
    # history
    last_visited = get_papers(app)
    paper_number = last_visited.get('PaperNumber', 1)
    page_number = last_visited.get('PageNumber', 1)
    history = { 
        "paper_number": paper_number,
        "page_number": page_number
    }
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = request.args.get(get_per_page_parameter(), type=int, default=20)
    total, papers = get_json_data(JSON_PATH, page, per_page)
    pagination = Pagination(page=page, per_page=per_page, 
                            total=total, search=search,
                            record_name='papers', css_framework='bootstrap4')

    return render_template('index.html', fixed="", solar=solar,
                            history=history, papers=papers, pagination=pagination)



# search history
@app.route('/status', methods=['GET', 'POST'])
def status():
    # show history in json file
    if request.method == 'GET':
        data = get_papers(app, True)
        response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )
        return response
    
    # update history
    if request.method == 'POST':
        paper_number = request.values.get('paperNumber')
        page_number = request.values.get('pageNumber')
        result = 'fail'
        status = 500
        if paper_number and page_number:
            changes = insert_papers(app, (paper_number, page_number))
            if changes:
                result = 'success'
                status = 200 
        response = app.response_class(
            response=json.dumps({'result': result}),
            status=status,
            mimetype='application/json'
        )
        return response            


# 404 error
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


