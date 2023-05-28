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
import smtplib
from email.message import EmailMessage

from selenium.webdriver.support.select import Select

config = configparser.ConfigParser()
config.read_file(open(r'config.txt'))
spire_log = config.get('Config', 'login')
spire_pass = config.get('Config', 'password')
search_start = config.get('Config', 'start')

service = Service(executable_path="/chromedriver_win32/chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(15)

if spire_pass == '' or spire_log == '' or search_start == '':
    print("One or more fields in the configuration file are empty. Please fill them in and try again.", sep=' ', end='\n', file=sys.stdout, flush=False)
    os.system("pause")
    sys.exit()

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

    #redirect to housing page
    driver.get('https://www.spire.umass.edu/psc/heproda_newwin/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_START_PAGE_FL.GBL?GMenu=SSR_STUDENT_FL&amp')
    time.sleep(3)

    #redirect to room selection page
    driver.get("https://www.spire.umass.edu/psc/heproda_newwin/EMPLOYEE/SA/c/UM_H_SELF_SERVICE_FL.UM_H_SS_RMSELHM_FL.GBL?NavColl=true")
    time.sleep(3)

    #click on search link
    room_search = driver.find_element(by=By.ID, value="UM_H_DRV_RS_HOM_UMH_RMSRCH_LNK")
    ActionChains(driver)\
        .click(room_search)\
        .perform()
    time.sleep(3)

    #switch to housing select iframe
    driver.switch_to.frame(driver.find_element(by=By.ID, value="ptModFrame_0"))

    #select correct year
    select_element = driver.find_element(by=By.ID, value="UM_H_DRV_RMSRCH_STRM")
    select = Select(select_element)
    select.select_by_value('1237')
    time.sleep(1)

    #select correct assignment
    assignment_element = driver.find_element(by=By.ID, value="UM_H_DRV_RMSRCH_UMH_APPT_TYPE")
    select_assignment = Select(assignment_element)
    select_assignment.select_by_value("123703JSRS")

    #select area
    #For North: UM_H_DRV_RMSRCH_UMH_RM_SRCH_SCOPE$10$
    #For All Residence Halls: UM_H_DRV_RMSRCH_UMH_RM_SRCH_SCOPE$68$
    
    area = driver.find_element(by=By.ID, value = "UM_H_DRV_RMSRCH_UMH_RM_SRCH_SCOPE$68$") 
    area.click()
    time.sleep(3)


    # For selecting building: 
    # select North:UM_H_DRV_RMSRCH_UMH_BLDG_GRP/*
    #area_select = driver.find_element(by=By.ID, value = "UM_H_DRV_RMSRCH_UMH_BLDG_GRP")
    #select_area = Select(area_select)
    #select_area.select_by_value("NO")
    #time.sleep(1)


    #Searches all available spaces
    vacant_areas = driver.find_element(by=By.ID, value = "UM_H_DRV_RMSRCH_UMH_RM_SRCH_QUAL1$93$")
    vacant_areas.click()
    time.sleep(1)

    #Clicks "Search"
    submit = driver.find_element(by=By.ID, value="UM_H_DRV_RMSRCH_SEARCH_PB$span")
    submit.click()
    time.sleep(1)

    room_count = 0
    while room_count == 0:
        grid = driver.find_element(by=By.CLASS_NAME, value="ps_grid-body")
        elements = grid.find_elements(by=By.TAG_NAME, value="tr")
        room_count = len(elements) - 1
        print(f"{room_count} rooms found")

        submit_new2 = driver.find_element(by=By.ID, value="UM_H_DRV_RSRCSL_UMH_NEW_SRCH_PB$span")
        submit_new2.click()
        time.sleep(1)

        #reselect assignment after going back
        assignment_element = driver.find_element(by=By.ID, value="UM_H_DRV_RMSRCH_UMH_APPT_TYPE")
        select_assignment = Select(assignment_element)
        select_assignment.select_by_value("123703JSRS")
        time.sleep(1)

        #resubmit
        submit_new = driver.find_element(by=By.ID, value="UM_H_DRV_RMSRCH_SEARCH_PB$span")
        submit_new.click()
        time.sleep(1)


 