from flask import Flask, redirect
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient() #connects to the local host, default port mongo server (which is what we have!)
db = client.db
collection = db['CS301']
print(collection.count_documents({}))

@app.route('/')
def index():
  return 'Server Works!'

# Returns a count of how many documents are in the collection
@app.route('/HW1')
def hw_1():
  return str(collection.count_documents({}))

# Returns the twitter_username and category_code for companies that have "Zoho" as a name of a stoneable of milestones
@app.route('/HW2')
def hw_2():
    doc_list = []
    for doc in collection.find({"milestones.stoneable.name":"Zoho"}, {"twitter_username": 1, "category_code": 1, "_id":0}):
        doc_list.append(str(doc))
    return "\n".join(doc_list)

# Returns the twitter_username for all documents
@app.route('/HW3')
def hw_3():
    doc_list = []
    for doc in collection.find({}, {"twitter_username":1, "_id":0}):
        doc_list.append(str(doc))
    return "\n".join(doc_list)

# Returns the name, founded_year, number_of_employees and total_money_raised for companies whose founded_year was
# after 2000 and whose number_of_employees was greater than or equal to 5000
@app.route('/HW4')
def hw_4():
    doc_list = []
    for doc in collection.find({"number_of_employees": {"$gte": 5000}, "founded_year": {"$gt": 2000}}, {"name":1, "founded_year":1, "number_of_employees":1, "total_money_raised":1,"_id":0}):
        doc_list.append(str(doc))
    return "\n".join(doc_list)

# Returns the _id for companies that do not have a founded_month field
@app.route('/HW6')
def hw_6():
    doc_list = []
    for doc in collection.find({"founded_month":{"$exists":"false"}}, {"_id":1}):
        doc_list.append(str(doc))
    return "\n".join(doc_list)

# Returns a count of the number of documents whose raised_amount of funding_rounds is greater than 5 million
@app.route('/HW7')
def hw_7():
    return str(collection.count_documents({"funding_rounds.raised_amount": {"$gt": 5000000}}))

# Returns the name and founded_year for companies whose founded_year was before 1805 or whose
# founded_year was after 2012. Sort by founded_year in descending order then by name in ascending order
@app.route('/HW9')
def hw_9():
    doc_list = []
    for doc in collection.find({"$or":[{"founded_year":{"$gt":2012}},{"founded_year": {"$lt":1805}}]}, {"_id":0, "name":1, "founded_year":1}).sort([("founded_year",-1), ("name",1)]):
        doc_list.append(str(doc))
    return "\n".join(doc_list)

# Returns the name, homeage_url, number_of_employees, and name of products for companies with
# a founded_year equal to 1800 and that have a name of products
@app.route('/HW10')
def hw_10():
    doc_list = []
    for doc in collection.find({"founded_year": 1800, "products.name": {"$exists": "true"}},{"name":1, "homepage_url":1, "number_of_employees":1, "products.name":1, "_id":0}):
        doc_list.append(str(doc))
    return "\n".join(doc_list)

# Returns a count of the documents whose attribution of screenshots is a null value
@app.route('/HW12')
def hw_12():
    return str(collection.find({"screenshots.attribution":{"$exists": "false"}}).count())

# Returns the maximum number_of_employees over all companies without using $max
@app.route('/HW13')
def hw_13():
    doc_list = []
    for doc in collection.find({}, {"number_of_employees": 1,"_id":0}).sort("number_of_employees",-1).limit(1):
        doc_list.append(str(doc))
    return "\n".join(doc_list)

#Returns a company document based on <COMPANY_NAME>.
#Returns a string saying "No Company Found" if no company name equals <COMPANY_NAME>
@app.route('/company/<COMPANY_NAME>')
def comp_name(COMPANY_NAME):
    for doc in collection.find({"name":COMPANY_NAME, "permalink":{"$exists":"true"}}):
        return str(doc)
    return "No Company Found"

#Returns all company documents (or top few documents) where their year founded is equal to the parameter <YEAR FOUNDED>.
#Return a string saying "No Companies Founded In The Year <YEAR_FOUNDED> is no company is found that year.
#Return an error page if the <YEAR_FOUNDED> field is not a 4 digit number.
@app.route('/list_companies_by_year/<YEAR_FOUNDED>')
def year_found(YEAR_FOUNDED):
    doc_list = []
    if len(YEAR_FOUNDED) != 4:
        return "ERROR: YEAR_FOUNDED must be a 4 digit number"
    for doc in collection.find({"founded_year": int(YEAR_FOUNDED), "permalink": {"$exists": "true"}}):
        doc_list.append(str(doc))
    if doc_list:
        return "\n".join(doc_list)
    return f"No Companies Founded In The Year {YEAR_FOUNDED}"

#Returns count of all companies where their year founded is equal to the parameter <YEAR FOUNDED>.
#Return a string saying "No Companies Founded In The Year <YEAR_FOUNDED> is no company is found that year.
#Return an error page if the <YEAR_FOUNDED> field is not a 4 digit number.
@app.route('/count_companies_by_year/<YEAR_FOUNDED>')
def year_count(YEAR_FOUNDED):
    if len(YEAR_FOUNDED) != 4:
        return "ERROR: YEAR_FOUNDED must be a 4 digit number"
    count = collection.find({"founded_year": int(YEAR_FOUNDED), "permalink": {"$exists": "true"}}).count()
    if count:
        return str(count)
    return f"No Companies Founded In The Year {YEAR_FOUNDED}"

#Find the company documents with the <COMPANY_NAME> and use a built-in Flask operation to
#redirect the user's web browser to the company's crunchbase URL located in the document.
#If no company is found, return an error message as above. Use the default HTTP status code for the redirect.
@app.route('/crunchbase/redirect/<COMPANY_NAME>')
def redirect_crunch(COMPANY_NAME):
    for doc in collection.find({"name":COMPANY_NAME, "permalink":{"$exists":"true"}}, {"_id":0, "crunchbase_url":1}):
        crunch_url = str(doc)
        crunch_url = crunch_url[20:-2]
        return redirect(crunch_url, code=302)
    return "No Company Found"
