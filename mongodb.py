from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient

load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://zimmermanalex13:{password}@coursers.elqhzuf.mongodb.net/?retryWrites=true&w=majority"


client = MongoClient(connection_string)
courses_db = client.courses\



collections = courses_db.list_collection_names()

print(collections)

#print documents in courses > subjects collections
subjects = courses_db.subjects
subjects_documents = subjects.find({})
for doc in subjects_documents:
    print(doc)

    
