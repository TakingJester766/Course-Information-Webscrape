from pymongo import MongoClient
import bson

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

def create_child_obj(course_obj):
    if course_obj.courseType == "lectureOnly":
        
        print("CREATE CHILD OBJ")
        print(course_obj.courseId)
        print(course_obj.meetingDays)
        print(course_obj.instructor)

        course = {
            "lectureSection": course_obj.courseId,
            "lectureTime": course_obj.meetingDays,
            "lectureInstructor": course_obj.instructor
        }
        child_obj_array.append(course)
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
    else:
        print("ERROR: Course type not found")


def create_parent_obj(course_title, course_type):
    print(child_obj_array)
    if course_type == "lectureOnly":
        course = {
            "courseName": course_title,
            "courseSections": [
                child_obj_array
            ]
        }
        print(course)
        courses_array.append(course)
    else:
        course = {
            "courseName": course_title,
            "courseSections": [
                child_obj_array
            ]
        }
        print(course)
        courses_array.append(course)
    


def upload_docs(subject_name):
    subjectDocument = {
        "subjectName": subject_name,
        "subjectCourses": courses_array
    }

    subjects.insert_one(subjectDocument)


'''
create_child_obj("lectureOnly", lecture_only_obj)

create_parent_obj("ACCOUNTG 371", "lectureOnly")

upload_docs("Accounting")


'''




#it works!
#upload_docs("Accounting", courses_array)

"""

{
      "courseName": "ACCOUNTG 371",
      "courseSections": [
        {
          "lectureSection": "Class 75028: Lecture 01",
          "lectureTime": "Monday Wednesday Friday 10:10AM to 11:00AM",
          "lectureInstructor": "Sean Wandrei"
        }
      ]
    },
    {
      "courseName": "ACCOUNTG 396H",
      "courseSections": [
        {
          "lectureSection": "Class 1000: Lecture 01",
          "lectureTime": "Monday Friday 10:10AM to 11:00AM",
          "lectureInstructor": "Jericho Albricht"
        }
      ]
    }

"""