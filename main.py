import os
import sys
import selenium
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.service import Service
import configparser
from selenium import webdriver
from subprocess import CREATE_NO_WINDOW
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.support.select import Select

from subjects_array import subjectArr

config = configparser.ConfigParser()
config.read_file(open(r'config.txt'))
spire_log = config.get('Config', 'login')
spire_pass = config.get('Config', 'password')
search_start = config.get('Config', 'start')

service = Service(executable_path="/chromedriver_win32/chromedriver.exe")
service.creationflags = CREATE_NO_WINDOW
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(15)

#example: <span class="ps_box-value" id="SSR_CRSE_INFO_V_SSS_SUBJ_CATLG">ANTHRO 105</span>
courseTitleId = "SSR_CRSE_INFO_V_SSS_SUBJ_CATLG"

#can assume that lecture and discussions/labs are all inside span tags

lectureId = "SSR_CLSRCH_F_WK_SSR_CMPNT_DESCR_1$294$$"
lectureMeetingTime = "SSR_CLSRCH_F_WK_SSR_MTG_SCHED_L_1$134$$"
lectureInstructor = "SSR_CLSRCH_F_WK_SSR_INSTR_LONG_1$86$$"


#discussion and lab query ids are the same
discussionOrLabId = "SSR_CLSRCH_F_WK_SSR_CMPNT_DESCR_2$295$$"
discussionOrLabMeetingTime = "SSR_CLSRCH_F_WK_SSR_MTG_SCHED_L_2$135$$"
discussionOrLabInstructor = "SSR_CLSRCH_F_WK_SSR_INSTR_LONG_2$161$$"

if spire_pass == '' or spire_log == '' or search_start == '':
    print("One or more fields in the configuration file are empty. Please fill them in and try again.", sep=' ', end='\n', file=sys.stdout, flush=False)
    os.system("pause")
    sys.exit()


#to have getCourseInformation return an object
class LectureOnly:
    def __init__(self, courseTitle, courseId, meetingDays, instructor):
        self.courseTitle = courseTitle
        self.courseId = courseId
        self.meetingDays = meetingDays
        self.instructor = instructor

#class for if lecture and lab in same course
class LectureAndLab:
    def __init__(self, courseTitle, courseId, meetingDays, instructor, labDays, labInstructor):
        self.courseTitle = courseTitle
        self.courseId = courseId
        self.meetingDays = meetingDays
        self.instructor = instructor
        self.labDays = labDays
        self.labInstructor = labInstructor

#for seminar classes
class Seminar:
    def __init__(self, courseTitle, courseId, meetingDays, instructor, seminarDays, seminarInstructor):
        self.courseTitle = courseTitle
        self.courseId = courseId
        self.meetingDays = meetingDays
        self.instructor = instructor
        self.seminarDays = seminarDays
        self.seminarInstructor = seminarInstructor

#getting number of rows in table after clicking on specific course
def getNumRows():
    tbody = driver.find_element(By.TAG_NAME, 'tbody')
    rows = tbody.find_elements(By.TAG_NAME, 'tr')
    return len(rows)

#get number of courses for a given subject
def getNumCourses():
    b_parent = driver.find_element(By.CLASS_NAME, "ps-htmlarea")
    b = b_parent.find_element(By.TAG_NAME, "b")
    return int(b.text)
    
def checkClassType():
    #checks what type of class in a given course. depending on if lecture only, lecture and lab, or seminar only, returns "lectureOnly", "lectureAndLab", or "seminar"
    #use checkIfLectureOnly, checkIfLectureAndLab, or checkIfSeminar methods
    
    #start with lecture and lab
    #labCheck checks if lab is present
    labCheck = driver.find_elements(By.ID, labId)
    if len(labCheck) > 0:
        print("lecture and lab")
        return "lectureLab"
    
        

#get information for lecture only classes
def getLectureOnly(row):

    courseTitle = driver.find_element(by=By.ID, value = courseTitleId)

    courseId = driver.find_element(by=By.ID, value = lectureId + str(row))
    meetingDays = driver.find_element(by=By.ID, value = lectureMeetingTime + str(row))
    instructor = driver.find_element(by=By.ID, value = lectureInstructor + str(row))
    
    course_info = LectureOnly(courseTitle.text, courseId.text, meetingDays.text, instructor.text)

    return course_info

#get information for lecture and lab classes
def getLectureAndLab(row):
    courseTitle = driver.find_element(by=By.ID, value="SSR_CRSE_INFO_VW_DESCR$0_row" + str(row))
    courseId = driver.find_element(by=By.ID, value="SSR_CLSRCH_F_WK_SSR_CMPNT_DESCR_1$294$$" + str(row))
    meetingDays = driver.find_element(by=By.ID, value="SSR_CLSRCH_F_WK_SSR_MTG_SCHED_L_1$134$$" + str(row))
    instructor = driver.find_element(by=By.ID, value="SSR_CLSRCH_F_WK_SSR_INSTR_LONG_1$86$$" + str(row))

    labDays = driver.find_element(by=By.ID, value="SSR_CLSRCH_F_WK_SSR_CMPNT_DESCR_2$295$$" + str(row)) 
    labStaff = driver.find_element(by=By.ID, value="SSR_CLSRCH_F_WK_SSR_INSTR_LONG_2$161$$" + str(row))

    courseInfo = LectureAndLab(courseTitle.text, courseId.text, meetingDays.text, instructor.text, labDays.text, labStaff.text)

    return courseInfo

#get information for seminar classes
def getSeminar(row):
    courseTitle  = driver.find_element(by=By.ID, value="SSR_CLSRCH_F_WK_SSR_CMPNT_DESCR_1$294$$" + str(row))
    courseId = driver.find_element(by=By.ID, value="SSR_CLSRCH_F_WK_SSR_MTG_SCHED_L_1$134$$" + str(row))
    meetingDays = driver.find_element(by=By.ID, value="SSR_CLSRCH_F_WK_SSR_MTG_DT_LONG_1$88$$" + str(row))
    instructor = driver.find_element(by=By.ID, value="SSR_CLSRCH_F_WK_SSR_INSTR_LONG_1$86$$" + str(row))

    courseInfo = Seminar(courseTitle.text, courseId.text, meetingDays.text, instructor.text  )

    return courseInfo

#courseTitleId: SSR_CRSE_INFO_V_SSS_SUBJ_CATLG

#lectureId: SSR_CLSRCH_F_WK_SSR_CMPNT_DESCR_1$294$$ + rowNum
#lectureMeetingTime: SSR_CLSRCH_F_WK_SSR_MTG_SCHED_L_1$134$$ + rowNum
#lectureInstructor: SSR_CLSRCH_F_WK_SSR_INSTR_LONG_1$86$$ + rowNum

#discussionTitleId: SSR_CLSRCH_F_WK_SSR_CMPNT_DESCR_2$295$$ + rowNum
#discussionMeetingTime: SSR_CLSRCH_F_WK_SSR_MTG_SCHED_L_2$135$$ + rowNum
#discussionInstructor: SSR_CLSRCH_F_WK_SSR_INSTR_LONG_2$161$$ + rowNum

#labId: SSR_CLSRCH_F_WK_SSR_CMPNT_DESCR_2$295$$ + rowNum
#labMeetingTime: SSR_CLSRCH_F_WK_SSR_MTG_SCHED_L_2$135$$ + rowNum
#labInstructor: SSR_CLSRCH_F_WK_SSR_INSTR_LONG_2$161$$ + rowNum

#gets course information from table
def getCourseInformation(row, courseType):
    if courseType == "lecture":
        course_info = getLectureOnly(row)
        print(course_info.courseTitle)
        print(course_info.courseId)
        print(course_info.meetingDays)
        print(course_info.instructor)
    elif courseType == "lectureLab":
        course_info = getLectureAndLab(row)
        print(course_info.courseTitle)
        print(course_info.courseId)
        print(course_info.meetingDays)
        print(course_info.instructor)
        print(course_info.labDays)
        print(course_info.labInstructor)
    elif courseType == "seminar":
        course_info = getSeminar(row)
        print(course_info.courseTitle)
        print(course_info.courseId)
        print(course_info.meetingDays)
        print(course_info.instructor)
        print(course_info.seminarDays)
        print(course_info.seminarInstructor)
    else:
        print("course type not found")

    return course_info
        
    
    
    
    
        
from selenium.common.exceptions import NoSuchElementException

#loop through subjects
def loopSubjects(subjectsArr):

    for subject in subjectsArr:

        #select additional ways to search button
        additional_ways_to_search = driver.find_element(by=By.ID, value="SSR_CLSRCH_FLDS_PTS_ADV_SRCH")
        ActionChains(driver)\
            .click(additional_ways_to_search)\
            .perform()
        time.sleep(4)

        driver.switch_to.frame(driver.find_element(by=By.ID, value="ptModFrame_0"))

        dropdown = driver.find_element(by=By.ID, value="SSR_CLSRCH_ADV_SSR_ADVSRCH_OP2$0")
        select = Select(dropdown)
        print(subject)
        select.select_by_visible_text(subject)

        search_btn = driver.find_element(by=By.ID, value="SSR_CLSRCH_FLDS_SSR_SEARCH_PB_1$0")
        ActionChains(driver)\
            .click(search_btn)\
            .perform()
           
        time.sleep(3)

        loopCourses()

        time.sleep(3)

def loopCourses():
    numCourses = getNumCourses()
    courseType = checkClassType()
    print(numCourses)

    foundCourses = 0

    i = 0
    while foundCourses < numCourses:
        try:
            #clicks specific course under a subject
            course_to_click = driver.find_element(by=By.ID, value="PTS_LIST_TITLE$" + str(i))
            ActionChains(driver).click(course_to_click).perform()
            time.sleep(3)

            print("checkpoint reached, starting loop")

            numRows = getNumRows()  # get the fresh number of rows for the new course
            for j in range(0, numRows):
                print("checking if lecture only, lecture and lab, or seminar")
                getCourseInformation(j, courseType)          

            time.sleep(3)
            driver.back()
            time.sleep(3)

            print("current i: " + str(i))

            foundCourses += 1  # increment foundCourses at the end of each successful iteration
            i += 1  # increment i at the end of each successful iteration

        except NoSuchElementException:
            print("Element not found. Incrementing i by 1. i currently: " + str(i))
            i += 1
            print("i incremented to: " + str(i))
            if i >= numCourses:
                print("No more courses to click. Exiting loop.")
                break
            continue

        #if all courses found, click this id: PT_WORK_PT_BUTTON_BACK
        if foundCourses == numCourses:
            back_btn = driver.find_element(by=By.ID, value="PT_WORK_PT_BUTTON_BACK")
            ActionChains(driver).click(back_btn).perform()
            time.sleep(3)
            break







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
    add_drop_edit_btn = driver.find_element(by=By.ID, value="SCC_LO_FL_WRK_SCC_VIEW_BTN$IMG$2")
    ActionChains(driver)\
        .click(add_drop_edit_btn)\
        .perform()
    time.sleep(3)

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

    

    

    

    
    loopSubjects(subjectArr)


            


            

            
            

    

    
        

    

    

#tbody class="ps_grid-body"

    



main()




