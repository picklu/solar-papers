from flask import Flask, escape, g, json, request, render_template
from flask_paginate import Pagination, get_page_parameter, get_per_page_parameter
from config import DATA, JSON_PATH


app = Flask(__name__)

from db import insert_papers, get_papers

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
    searched = get_papers(False)
    history = {
        'paper': searched.get('paperNumber', 1),
        'page': searched.get('pageNumber', 1)
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
        all = request.args.get('q', 'last')
        data = {'error': 'Did not undestand what you wanted!'}
        if all == 'all':
            data = get_papers()
        elif all == 'last':
            data = get_papers(False)
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
        time_stamp = request.values.get('timeStamp')
        data = {
            "paperNumber": paper_number, 
            "pageNumber": page_number,
            "timeStamp": time_stamp
        }
        result = 'fail'
        status = 500
        if paper_number and page_number:
            changes = insert_papers(data)
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


