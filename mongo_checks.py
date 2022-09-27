import pymongo
import pandas as pd
import numpy as np

db = pymongo.MongoClient("gigas.clipit.es", 21000)

db = db["cstrack"]

print(db.list_collection_names())

col = db["statuses_extended"]

col.drop()

print(db.list_collection_names())