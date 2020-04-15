from flask_pymongo import PyMongo
from papers import app
from urllib import parse

from config import DB_USER, DB_PASS, DB_URI

db_user = parse.quote_plus(DB_USER)
db_pass = parse.quote_plus(DB_PASS)
db_uri = DB_URI %(db_user, db_pass)
app.config["MONGO_URI"] = db_uri
mongo = PyMongo(app)


def OI_to_str(doc):
    new_doc = {}
    doc = doc if isinstance(doc, dict) else {}
    for key in doc.keys():
        if key == "_id":
            new_doc[key] = str(doc[key])
        else:
            new_doc[key] = doc[key]
    return new_doc


def insert_papers(args):
    id = mongo.db.papers.insert_one(args).inserted_id
    return 1 if id else 0


def get_papers(all=True):
    docs = [OI_to_str(doc) for doc in mongo.db.papers.find({})]
    if all:
        return docs
    return {} if not docs else docs[-1]


def clear_papers():
    pageNumber = get_papers(False).get('pageNumber') 
    return mongo.db.papers.remove( {'pageNumber': {'$lt': pageNumber}})