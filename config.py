from os import environ, path


DATA = path.join(path.dirname(__file__), "data")
JSON_PATH = path.join(DATA, "papers.json")
DB_USER = environ["DB_USER"]
DB_PASS = environ["DB_PASS"]
DB_URI = "mongodb://%s:%s@ds035137.mlab.com:35137/solarpapers?retryWrites=false"