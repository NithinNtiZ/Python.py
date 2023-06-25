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
        "name" : "nithin",
        "age"  : "30"
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
    age= [1,2,3,4,5]
    docs=[]

    for firstname, age in zip(firstname, age):
        doc  = { "firstname" : firstname, "age": age}
        docs.append(doc)

    collection.insert_many(docs)
    print(docs)

create_document()
    
