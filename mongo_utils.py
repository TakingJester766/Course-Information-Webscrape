from pymongo import MongoClient
import json

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
        print(f"Encountered a syntax error when trying to evaluate a dictionary: {e}")
        return child_obj_array  # Return the original list if a syntax error occurs


def create_child_obj(course_obj):
    global child_obj_array
    if course_obj.courseType == "lectureOnly":
        
        #print("CREATE CHILD OBJ")
        #print(course_obj.courseId)
        #print(course_obj.meetingDays)
        #print(course_obj.instructor)

        course = {
            "lectureSection": course_obj.courseId,
            "lectureTime": course_obj.meetingDays,
            "lectureInstructor": course_obj.instructor
        }
        child_obj_array.append(course)
        child_obj_array = remove_duplicates(child_obj_array)

        print("HERE IS THE CHILD COURSE OBJ: " + str(course) + "\n")
        print("HERE IS THE CHILD OBJ ARRAY: " + str(child_obj_array) + "\n")
    elif course_obj.courseType == "lectureLab":
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

        print("HERE IS THE CHILD COURSE OBJ: " + str(course) + "\n")
        print("HERE IS THE CHILD OBJ ARRAY: " + str(child_obj_array) + "\n")
    else:
        print("ERROR: Course type not found")


def create_parent_obj(course_title, course_type):
    #print(child_obj_array)
    if course_type == "lectureOnly":
        course = {
            "courseName": course_title,
            "courseSections": [
                list(child_obj_array)
            ]
        }
        print("HERE IS THE PARENT COURSE OBJ: " + str(course) + "\n")
        courses_array.append(course)
    else:
        course = {
            "courseName": course_title,
            "courseSections": [
                list(child_obj_array)
            ]
        }
        print("HERE IS THE PARENT COURSE OBJ: " + str(course) + "\n")
        courses_array.append(course)
    child_obj_array.clear()
    


def upload_docs(subject_name):
    print("COURSES ARRAY CONTENTS: " + str(courses_array) + "\n")
    subjectDocument = {
        "subjectName": subject_name,
        "subjectCourses": courses_array
    }

    subjects.insert_one(subjectDocument)
    print("Success, clearning courses array")
    courses_array.clear()
    


