import csv
from os import path
from flask import Flask, escape, json, jsonify, request

app = Flask(__name__)

folder = path.join(path.dirname(__file__), "data")

def get_json_data(filename, start, length):
    with open(filename) as infile:
        data = json.load(infile)["data"]
        return jsonify({"data": data[start : start + length]})


@app.route('/')
def home():
    name = request.args.get("name", "World")

    if name == "dsscs" or name == "prscs":
        start = int(request.args.get("start", 0))
        length = int(request.args.get("length", 50))
        filepath = path.join(folder, f"{name}_papers.json")
        return get_json_data(filepath, start, length)
    else:
        return f"Hello, {escape(name)}! It works."


