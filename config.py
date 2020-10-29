from os import environ, path


DATA = path.join(path.dirname(__file__), "data")
JSON_PATH = path.join(DATA, "papers.json")
DB_USER = environ["DB_USER"]
DB_PASS = environ["DB_PASS"]
DB_URI = "mongodb+srv://%s:%s@solarpapers.3z8k0.mongodb.net/solarpapers?retryWrites=true&w=majority"