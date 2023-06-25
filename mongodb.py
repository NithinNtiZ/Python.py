from pymongo import MongoClient
import pprint
import os
import json
import subprocess
import re
""" import requests
import beautifulsoap """


connection_string = "mongodb://localhost:27017"
client = MongoClient(connection_string)

#show list of all dbs
db=client.list_database_names()

#access db
test_db=client.test

#acces collections
collection=test_db.list_collection_names()

print(collection)

#Insert data to documents
def insert_test_doc():
    collection=test_db.test_collection
    test_document= {
        "firstname" : "nithin",
        "age"  : "30",
        "place" : "china"
    }
    insert_ID=collection.insert_one(test_document).inserted_id
    print(insert_ID)

insert_test_doc()

#Insert multiple data to documents
""" production =client.production
person_collection=production.person_collection """

collection=test_db.test_collection
def create_document():
    firstname= ["one","two","three","four","five"]
    place= ["India","Japan","England","Nepal","USA",]
    age= [11,21,38,54,59]
    docs=[]

    for firstname, age, place in zip(firstname, age, place):
        doc  = { "firstname" : firstname, "age": age, "place": place}
        docs.append(doc)

    collection.insert_many(docs)
    print(docs)

create_document()

#search data in documents

printer= pprint.PrettyPrinter()
    
def find_all_person():
    for person in collection.find():
        printer.pprint(person)
find_all_person()

def find_nithin():
    nithin= collection.find_one({"name" : "nithin"})
    printer.pprint(nithin)
find_nithin()

def count():
    count= collection.count_documents(filter={})
    print("Number of document ", count)
count()

def find_ranage_age(min_age, max_age):
    query = {"$and" :[
        {"age" : {"$gte": min_age}},
        {"age" : {"$lte": max_age}}
    ]
    }
    person= collection.find(query).sort("age")
    for person in person:
        printer.pprint(person)
find_ranage_age(15, 40)

def project_coloum():
    coloum= {"_id": 0, "firstname": 1, "age": 1, "place" : 1}
    person= collection.find({}, coloum)
    for person in person:
        printer.pprint(person)
project_coloum()

