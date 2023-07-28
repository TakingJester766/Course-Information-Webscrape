from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
from firebase_admin import credentials, firestore
from bson.json_util import dumps
import os
import json
import firebase_admin

load_dotenv(find_dotenv())

auto_path = os.environ.get("AUTH_PATH")

password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://zimmermanalex13:{password}@coursers.elqhzuf.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(connection_string)
courses_db = client.courses
subjects = courses_db.subjects

# Use a service account
cred = credentials.Certificate(auto_path)
firebase_admin.initialize_app(cred)

db = firestore.client()

def export_subject_to_firestore(subject_name):
    subject = subjects.find_one({"subjectName": subject_name})

    if subject:
        # MongoDB uses ObjectId for _id which is not JSON serializable,
        # we need to convert it to string before we can dump to JSON
        subject["_id"] = str(subject["_id"])

        # Convert subject dictionary to Firestore acceptable format
        firestore_subject = json.loads(dumps(subject))

        # Remove _id field from firestore_subject
        del firestore_subject["_id"]

        # Add a new doc in collection 'courses' with ID of subjectName
        db.collection('courses').document(firestore_subject["subjectName"]).set(firestore_subject)
        
        print(f"Exported {subject_name} to Firestore.")
        
    else:
        print(f"No document found for subject: {subject_name}")


def update_sections_in_firestore(subject_name):
    # Retrieve the document
    doc_ref = db.collection('courses').document(subject_name)
    doc = doc_ref.get()
    
    if doc.exists:
        firestore_subject = doc.to_dict()

        # Add 'isActive' field to each section
        for course in firestore_subject.get("subjectCourses", []):
            for section in course.get("courseSections", []):
                section["isActive"] = False

        # Update the document
        doc_ref.set(firestore_subject)
        
        print(f"Updated {subject_name} in Firestore.")
    else:
        print(f"No document found for subject: {subject_name}")

export_subject_to_firestore("Accounting")
update_sections_in_firestore("Accounting")