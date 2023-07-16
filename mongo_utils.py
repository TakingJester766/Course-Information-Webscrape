from pymongo import MongoClient
import asyncio

from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient

load_dotenv(find_dotenv())

class MongoDBManager:
    def __init__(self, courses, subjects):
        self.client = MongoClient()
        self.db = self.client[courses] # change 'db_name' to your database name
        self.collection = self.db[subjects] # change 'collection_name' to your collection name

password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://zimmermanalex13:{password}@coursers.elqhzuf.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(connection_string)
courses_db = client.courses\

subjects = courses_db.subjects


courses_array = []
child_obj_array = []

#lecture_only_obj = LectureOnly("ACCOUNTG 371", "Class 75028: Lecture 01", "Monday Wednesday Friday 10:10AM to 11:00AM", "Sean Wandrei")


#necessary to fix inconsistencies in the data coming from Spire
def remove_duplicates(child_obj_array):
    try:
        temp_set = set(map(lambda x: str(x), child_obj_array))  # Convert dicts to strings and add to a set to remove duplicates
        return list(map(lambda x: eval(x), temp_set))  # Convert strings back to dicts
    except SyntaxError as e:
        print(f"Encountered a syntax error when trying to evaluate a dictionary: {e} \n")
        print("PROBLEM DICTIONARY: " + str(child_obj_array) + "\n")
        return child_obj_array  # Return the original list if a syntax error occurs


async def create_child_obj(course_obj):
    global child_obj_array
    if course_obj.courseType == "lectureOnly":

        #remove "\n" from meeting times
        course_obj.meetingDays = course_obj.meetingDays.replace("\n", " ")

        course = {
            "lectureSection": course_obj.courseId,
            "lectureTime": course_obj.meetingDays,
            "lectureInstructor": course_obj.instructor
        }
        child_obj_array.append(course)
        child_obj_array = remove_duplicates(child_obj_array)

    elif course_obj.courseType == "lectureLab":

        #remove "\n" from meeting times
        course_obj.meetingDays = course_obj.meetingDays.replace("\n", " ")
        course_obj.labDays = course_obj.labDays.replace("\n", " ")

        course = {
            "lectureSection": course_obj.courseId,
            "lectureTime": course_obj.meetingDays,
            "lectureInstructor": course_obj.lectureInstructor,
            "labSection": course_obj.labId,
            "labTime": course_obj.labDays,
            "labInstructor": course_obj.labInstructor
        }
        child_obj_array.append(course)
        child_obj_array = remove_duplicates(child_obj_array)

    else:
        print("ERROR: Course type not found")

async def create_parent_obj(course_title, subject_name):
    global child_obj_array
    global subjects

    course = {
        "courseName": course_title,
        "courseSections": list(child_obj_array)
    }

    # Insert/Update the course into the MongoDB collection
    subjects.update_one({"subjectName": subject_name}, {"$push": {"subjectCourses": course}}, upsert=True)
    child_obj_array.clear()
    print("Uploaded and child array cleared")
    

'''
def upload_docs(subject_name):
    print("COURSES ARRAY CONTENTS: " + str(courses_array) + "\n")
    subjectDocument = {
        "subjectName": subject_name,
        "subjectCourses": courses_array
    }

    subjects.insert_one(subjectDocument)
    print("Success, clearning courses array")
    courses_array.clear()
'''
