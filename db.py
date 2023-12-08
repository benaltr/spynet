from datetime import datetime
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING

cluster = MongoClient("mongodb://localhost:27017")
db = cluster["spynet"]
coll_history = db["history"]
coll_rules = db["rules"]

first_date = datetime.strptime(coll_history.find_one(sort=[("_id", ASCENDING)])["time"].split(" ")[0], '%Y-%m-%d')
last_date = datetime.strptime(coll_history.find_one(sort=[("_id", DESCENDING)])["time"].split(" ")[3], '%Y-%m-%d')

