from pymongo import MongoClient
from bson.objectid import ObjectId

from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient

load_dotenv(find_dotenv())

class MongoDBManager:
    def __init__(self, db_name, collection_name):
        self.client = MongoClient()
        self.db = self.client[db_name] # change 'db_name' to your database name
        self.collection = self.db[collection_name] # change 'collection_name' to your collection name


password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://zimmermanalex13:{password}@coursers.elqhzuf.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(connection_string)
courses_db = client.courses\

def save_subject(self, subject, courses):
    # 'subject' should be a string representing the subject name.
    # 'courses' should be a list of course dictionaries.
    subject_doc = {
        'subjectName': subject,
        'subjectCourses': courses,
    }
    self.collection.insert_one(subject_doc)
