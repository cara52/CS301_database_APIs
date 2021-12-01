from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient() #connects to the local host, default port mongo server (which is what we have!)

@app.route('/')
def index():
  return 'Server Works!'
  
@app.route('/count')
def get_count():
  return str(client.db['CS301'].count_documents({}))

@app.route('/hw_test')
def hw_query_test():
  array = {}
  i = 0
  for doc in client.db['CS301'].find({"founded_year": 1901}, {"name": 1, "permalink": 1, "_id": 0}):
    array[i] = doc
    i += 1
  return array

@app.route('/example')
def example():
  doc = client.db['CS301'].find_one({"founded_year": 1999})
  return str(doc['name'])