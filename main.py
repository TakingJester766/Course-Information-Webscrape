import os
import sys
import time
import configparser
from subprocess import CREATE_NO_WINDOW

from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException

import asyncio

from subjects_array import subjects_array

#imports for mongodb
from mongo_utils import create_child_obj, create_parent_obj


config = configparser.ConfigParser()
config.read_file(open(r'config.txt'))
spire_log = config.get('Config', 'login')
spire_pass = config.get('Config', 'password')
search_start = config.get('Config', 'start')

service = Service(executable_path="/chromedriver_win32/chromedriver.exe")
service.creationflags = CREATE_NO_WINDOW
driver = webdriver.Chrome(service=service)

#example: <span class="ps_box-value" id="SSR_CRSE_INFO_V_SSS_SUBJ_CATLG">ANTHRO 105</span>
courseTitleId = "SSR_CRSE_INFO_V_SSS_SUBJ_CATLG"

#can assume that lecture and discussions/labs are all inside span tags


lectureId = "SSR_CLSRCH_F_WK_SSR_CMPNT_DESCR_1$294$$"
lectureMeetingTime = "SSR_CLSRCH_F_WK_SSR_MTG_SCHED_L_1$134$$"
lectureInstructorId  = "SSR_CLSRCH_F_WK_SSR_INSTR_LONG_1$86$$"

search_id_reg = "PTS_LIST_TITLE$"
search_id_wind = "win8divPTS_LIST_TITLE$"


#discussion and lab query ids are the same
discussionOrLabId = "SSR_CLSRCH_F_WK_SSR_CMPNT_DESCR_2$295$$"
discussionOrLabMeetingTime = "SSR_CLSRCH_F_WK_SSR_MTG_SCHED_L_2$135$$"
discussionOrLabInstructor = "SSR_CLSRCH_F_WK_SSR_INSTR_LONG_2$161$$"

#wait for element to load
timeout = 20
wait = WebDriverWait(driver, timeout)


if spire_pass == '' or spire_log == '' or search_start == '':
    print("One or more fields in the configuration file are empty. Please fill them in and try again.", sep=' ', end='\n', file=sys.stdout, flush=False)
    os.system("pause")
    sys.exit()


#to have getCourseInfo return an object
class LectureOnly:
    def __init__(self, courseId, meetingDays, instructor):
        self.courseType = "lectureOnly"
        self.courseId = courseId
        self.meetingDays = meetingDays
        self.instructor = instructor

#class for if lecture and lab in same course
class LectureAndLab:
    def __init__(self, courseId, meetingDays, lectureInstructor, labId, labDays, labInstructor):
        self.courseType = "lectureLab"
        self.courseId = courseId
        self.meetingDays = meetingDays
        self.lectureInstructor = lectureInstructor
        self.labId = labId
        self.labDays = labDays
        self.labInstructor = labInstructor

#for writing to error log
def writeErrorLog(course_title, subject, error):
    try:
        with open("error_log.txt", "a") as error_log:
            error_log.write(f"Error uploading {course_title} in {subject} to database.\nError: {error}\n")
            error_log.write('-' * 30 + "\n")
    except Exception as e:
        print(f"An error occurred while writing to the error log: {e}")



#getting number of sections in table after clicking on specific course
def getNumRows():
    tbody = driver.find_element(By.TAG_NAME, 'tbody')
    rows = tbody.find_elements(By.TAG_NAME, 'tr')
    return len(rows)

#get number of courses for a given subject
def getNumCourses():
    b_parent = driver.find_element(By.CLASS_NAME, "ps-htmlarea")
    b = b_parent.find_element(By.TAG_NAME, "b")
    return int(b.text)

#will be used to created a variable dictating what type of class a given course is. For example, if a course has a lecture and lab, it will be a lectureLab type
def classifyCourseType():
    #checks what type of class in a given course. depending on if lecture only, lecture and lab, or seminar only, returns "lecture", "lectureLab", or "seminar"
    #use checkIfLectureOnly, checkIfLectureAndLab, or checkIfSeminar methods
    
    #Check if lecture and lab/discussion
    #check if lab or discussion section is present
    
    lectureCheck = driver.find_elements(by=By.ID, value = lectureId + "0")
    labCheck = driver.find_elements(by=By.ID, value = discussionOrLabId + "0")
    
    if (len(lectureCheck) > 0) and (len(labCheck) > 0):
        return "lectureLab"
    else:
        return "lecture"
    
#checks if no courses are present in a given subject
def check_no_results():
    try:
        # Find the element by its ID
        no_results_element = driver.find_element(by=By.ID, value="PTS_SRCH_PTS_INDEXTIME")

        # Check if the element's text is the "No results" message
        if no_results_element.text == "No results were returned. Refine your search by entering a different keyword.":
            return True
        else:
            print("Results present.\n")
            return False
    except NoSuchElementException:
        # If the element wasn't found, return False
        return False


def getCourseInfo(row, courseType):

    
    if (courseType == "lectureLab"):
        # do a for loop after classifying

        course_title = driver.find_element(by=By.ID, value=courseTitleId)
        print("course title: " + course_title.text)                
        
        courseId = driver.find_element(by=By.ID, value=lectureId + str(row))
        print("course id: " + courseId.text)
        meetingDays = driver.find_element(by=By.ID, value=lectureMeetingTime + str(row))
        print("meeting days: " + meetingDays.text)
        lectureInstructor = driver.find_element(by=By.ID, value=lectureInstructorId + str(row))
        print("instructor: " + lectureInstructor.text)

        labId = driver.find_element(by=By.ID, value=discussionOrLabId + str(row))
        print("lab id: " + labId.text)
        labDays = driver.find_element(by=By.ID, value=discussionOrLabMeetingTime + str(row))
        print("lab days: " + labDays.text) 
        labInstructor = driver.find_element(by=By.ID, value=discussionOrLabInstructor + str(row))
        print("lab staff: " + labInstructor.text + " \n")

        courseInfo = LectureAndLab(courseId.text, meetingDays.text, lectureInstructor.text, labId.text, labDays.text, labInstructor.text)
    else:
        
        course_title = driver.find_element(by=By.ID, value=courseTitleId)
        print("course title: " + course_title.text)

        courseId = driver.find_element(by=By.ID, value=lectureId + str(row))
        print("course id: " + courseId.text)

        meetingDays = "Multiple meeting schedules"  # Default value in case of exception

        try:
            meetingDaysTemp = driver.find_element(by=By.ID, value=lectureMeetingTime + str(row))
            meetingDays = meetingDaysTemp.text
            print("meeting days: " + meetingDays)
        except NoSuchElementException:
            pass  # Meeting days will remain as the default value

        instructor = driver.find_element(by=By.ID, value=lectureInstructorId + str(row))
        print("instructor: " + instructor.text + " \n")

        courseInfo = LectureOnly(courseId.text, meetingDays, instructor.text)


    return courseInfo

#loop through subjects
def loopSubjects(subjects_array):

    for subject in subjects_array:

        time.sleep(3)

        #select additional ways to search button
        additional_ways_to_search = wait.until(EC.visibility_of_element_located((By.ID, "SSR_CLSRCH_FLDS_PTS_ADV_SRCH")))
        #additional_ways_to_search = driver.find_element(by=By.ID, value="SSR_CLSRCH_FLDS_PTS_ADV_SRCH")
        ActionChains(driver)\
            .click(additional_ways_to_search)\
            .perform()
        time.sleep(3)

        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ptModFrame_0")))
        #driver.switch_to.frame(driver.find_element(by=By.ID, value="ptModFrame_0"))

        dropdown = wait.until(EC.visibility_of_element_located((By.ID, "SSR_CLSRCH_ADV_SSR_ADVSRCH_OP2$0")))
        #dropdown = driver.find_element(by=By.ID, value="SSR_CLSRCH_ADV_SSR_ADVSRCH_OP2$0")
        select = Select(dropdown)
        print(subject)
        select.select_by_visible_text(subject)


        search_btn = wait.until(EC.visibility_of_element_located((By.ID, "SSR_CLSRCH_FLDS_SSR_SEARCH_PB_1$0")))
        #search_btn = driver.find_element(by=By.ID, value="SSR_CLSRCH_FLDS_SSR_SEARCH_PB_1$0")
        ActionChains(driver)\
            .click(search_btn)\
            .perform()
        
        loopCourses(subject)

def loopCourses(subject):
    
    foundCourses = 4
    i = 9
    firstIteration = True
    missed_courses = 0

    try:
        #makes all classes visible
        all_classes_btn = wait.until(EC.visibility_of_element_located((By.ID, "PTS_BREADCRUMB_PTS_IMG$0")))
        #all_classes_btn = driver.find_element(by=By.ID, value="PTS_BREADCRUMB_PTS_IMG$0")
        ActionChains(driver)\
            .click(all_classes_btn)\
            .perform()
        time.sleep(3)
    except (NoSuchElementException, TimeoutException, StaleElementReferenceException) as e:
        print("All classes button not found. Continuing to next step.\n")
        pass
    
    numCourses = getNumCourses()
    print("Number of courses: " + str(numCourses))    
    
    missed_course_buffer = round(numCourses * 0.25)

    print("Missed course buffer: " + str(missed_course_buffer) + "\n")

    while foundCourses < numCourses:

        try:
            if not firstIteration:
                all_classes_btn = wait.until(EC.visibility_of_element_located((By.ID, "PTS_BREADCRUMB_PTS_IMG$0")))
                #all_classes_btn = driver.find_element(by=By.ID, value="PTS_BREADCRUMB_PTS_IMG$0")
                ActionChains(driver)\
                    .click(all_classes_btn)\
                    .perform()
                
                time.sleep(3)
            else:
                firstIteration = False
                time.sleep(3)
        except (NoSuchElementException, TimeoutException) as e:
            print("All classes button not found. Continuing to next step.")

        try:

            
            time.sleep(3)
            
            course_reg = driver.find_elements(by=By.ID, value=search_id_reg + str(i))
            course_wind = driver.find_elements(by=By.ID, value=search_id_wind + str(i))

            if (len(course_reg) > 0):
                course_to_click = wait.until(EC.visibility_of_element_located((By.ID, search_id_reg + str(i))))
                #course_to_click = driver.find_element(by=By.ID, value=search_id_reg + str(i))
                ActionChains(driver).click(course_to_click).perform()
            elif (len(course_wind) > 0):
                course_to_click = wait.until(EC.visibility_of_element_located((By.ID, search_id_wind + str(i))))
                #course_to_click = driver.find_element(by=By.ID, value=search_id_wind + str(i))
                ActionChains(driver).click(course_to_click).perform()
            else:
                #throw exception to increment i and continue
                raise NoSuchElementException

            course_title = wait.until(EC.visibility_of_element_located((By.ID, courseTitleId)))
            textTitle = course_title.text
            
            #need to wait for first element to appear also
            wait.until(EC.visibility_of_element_located((By.ID, lectureId + "0")))

            #course_title = driver.find_element(by=By.ID, value=courseTitleId)
            print("course title: " + textTitle)

            numRows = getNumRows()  # get the fresh number of rows for the new course

            courseType = classifyCourseType()
            #print("Course type: " + str(courseType) + "\n")

            #need to wait for first element to appear also
            wait.until(EC.visibility_of_element_located((By.ID, lectureId + "0")))

            for j in range(0, numRows):

                try:
                    #print("getting course information for row: " + str(j) + "\n")
                    
                    course_obj = getCourseInfo(j, courseType)

                    time.sleep(3)

                    asyncio.run(create_child_obj(course_obj))
                except (NoSuchElementException, TimeoutException, StaleElementReferenceException) as e:
                    print("Error getting course info for row: " + str(j) + "\n")
                    continue
                

            #will be used as a try/except for if a course is not found or can't upload. will write to error log if so, then go back to uploading courses.
            try:
                asyncio.run(create_parent_obj(textTitle, subject))
                #mongo_utils.child_obj_array.clear()  # putting it here returns empty arrays


                foundCourses += 1  # increment foundCourses at the end of each successful iteration
                i += 1  # increment i at the end of each successful iteration
                

                print("foundCourses: " + str(foundCourses) + "\ni: " + str(i) + "\n")
                

                driver.back()
                time.sleep(3)
            except:
                print("Error uploading to db\n")
                foundCourses += 1
                driver.back()
                time.sleep(3)
                continue
                
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException) as e:

            if (i < numCourses + missed_course_buffer):

                print("i SKIPPED AT " + str(i) + "\n")
                i += 1  # increment i only in the exception, if a course was not found
                missed_courses += 1
                continue
            else:
                print("i surpassed numCourses + buffer, exiting subject " + subject + "\n")
                break

    #once all courses found, exits loop. uploads to db then goes to next subject.

    #After exiting while loop, signifies that all courses have been found for the given subject. Click back button to return to search page and start next subject
    back_btn = wait.until(EC.visibility_of_element_located((By.ID, "PT_WORK_PT_BUTTON_BACK")))
    #back_btn = driver.find_element(by=By.ID, value="PT_WORK_PT_BUTTON_BACK")
    ActionChains(driver).click(back_btn).perform()
    time.sleep(3)


# MAIN METHOD, RUNS EVERYTHING
def main(time=time):    
    # log into spire using driver
    driver.get("https://www.umass.edu/it/spire")
    driver.maximize_window()
    spirelogbtn = driver.find_element(by=By.LINK_TEXT, value="Log in to SPIRE")
    ActionChains(driver)\
        .click(spirelogbtn)\
        .pause(1)\
        .perform()
    netidfield = driver.find_element(by=By.ID, value="userid")
    netpassfield = driver.find_element(by=By.ID, value="pwd")
    subfield = driver.find_element(by=By.NAME, value="Submit")
    ActionChains(driver)\
        .click(netidfield)\
        .pause(1)\
        .send_keys(spire_log)\
        .pause(1)\
        .click(netpassfield)\
        .pause(1)\
        .send_keys(spire_pass)\
        .pause(1)\
        .click(subfield)\
        .perform()

    #redirect to academics page
    driver.get('https://www.spire.umass.edu/psc/heproda_22/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_MD_SP_FL.GBL?Action=U&MD=Y&GMenu=SSR_STUDENT_FL&GComp=SSR_START_PAGE_FL&GPage=SSR_START_PAGE_FL&scname=CS_SSR_MANAGE_CLASSES_NAV&AJAXTransfer=y')
    time.sleep(3)

    #redirect to room selection page
    #driver.get("https://www.spire.umass.edu/psc/heproda_newwin/EMPLOYEE/SA/c/UM_H_SELF_SERVICE_FL.UM_H_SS_RMSELHM_FL.GBL?NavColl=true")    

    #switch to add drop edit dropdown
    add_drop_edit_btn = wait.until(EC.visibility_of_element_located((By.ID, "SCC_LO_FL_WRK_SCC_VIEW_BTN$IMG$2")))
    #add_drop_edit_btn = driver.find_element(by=By.ID, value="SCC_LO_FL_WRK_SCC_VIEW_BTN$IMG$2")
    ActionChains(driver)\
        .click(add_drop_edit_btn)\
        .perform()
    time.sleep(4)

    #navigate to search add enroll button
    search_add_enroll_btn = driver.find_element(by=By.ID, value="SCC_LO_FL_WRK_SCC_VIEW_BTN$24$$11")
    ActionChains(driver)\
        .click(search_add_enroll_btn)\
        .perform()
    time.sleep(3)

    #select relevant school term
    fall_semester = driver.find_element(by=By.ID, value="SSR_CSTRMCUR_VW_DESCR$1")
    ActionChains(driver)\
        .click(fall_semester)\
        .perform()
    time.sleep(3)
    
    loopSubjects(subjects_array)

main()




