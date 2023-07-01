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

class LectureOnly:
    def __init__(self, courseTitle, courseId, meetingDays, instructor):
        self.courseType = "lectureOnly"
        self.courseTitle = courseTitle
        self.courseId = courseId
        self.meetingDays = meetingDays
        self.instructor = instructor

class LectureAndLab:
    def __init__(self, courseTitle, courseId, meetingDays, lectureInstructor, labId, labDays, labInstructor):
        self.courseType = "lectureLab"
        self.courseTitle = courseTitle
        self.courseId = courseId
        self.meetingDays = meetingDays
        self.lectureInstructor = lectureInstructor
        self.labId = labId
        self.labDays = labDays
        self.labInstructor = labInstructor


password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://zimmermanalex13:{password}@coursers.elqhzuf.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(connection_string)
courses_db = client.courses\

subjects = courses_db.subjects

courses_array = [

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

]

def create_and_append_obj(course_obj):
    if course_obj.courseType == "lectureOnly":
        course = {
            "courseName": course_obj.courseTitle,
            "courseSections": [
                {
                    "lectureSection": course_obj.courseId,
                    "lectureTime": course_obj.meetingDays,
                    "lectureInstructor": course_obj.instructor
                }
            ]
        }
        courses_array.append(course)
    else:
        course = {
            "courseName": course_obj.courseTitle,
            "courseSections": [
                {
                    "lectureSection": course_obj.courseId,
                    "lectureTime": course_obj.meetingDays,
                    "lectureInstructor": course_obj.lectureInstructor
                },
                {
                    "labSection": course_obj.labId,
                    "labTime": course_obj.labDays,
                    "labInstructor": course_obj.labInstructor

                }
            ]
        }
        courses_array.append(course)



# The document you want to insert
#document = {
#    "subjectName": "Accounting",
#    "subjectCourses": [
        
#        courses_array[0]
            
        
#    ]
#}

# Insert the document
#ubjects.insert_one(document)

# to add to the subjectCourses array:

# The new course you want to add
# The new course you want to add
#new_course = courses_array[1]
                
            



# Use the $push operator to add the new course to the subjectCourses array
#subjects.update_one(
#    {"subjectName": "Accounting"}, 
#    {"$push": {"subjectCourses": new_course}}
#)


#read all courses in Account subjectName:
#accounting = subjects.find_one({"subjectName": "Accounting"})
#print(accounting)

#automate looping through all courses in array and adding them to given subjectName

#subjectDocument = {
#    "subjectName": "Accounting",
#    "subjectCourses": courses_array
#}

def upload_docs(subject_name, courses_array):
    subjectDocument = {
        "subjectName": subject_name,
        "subjectCourses": courses_array
    }

    subjects.insert_one(subjectDocument)




#it works!
#upload_docs("Accounting", courses_array)

