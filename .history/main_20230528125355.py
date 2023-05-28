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
service.creationflags = CREATE_NO_WINDOW
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

    #redirect to academics page
    driver.get('https://www.spire.umass.edu/psc/heproda_22/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_MD_SP_FL.GBL?Action=U&MD=Y&GMenu=SSR_STUDENT_FL&GComp=SSR_START_PAGE_FL&GPage=SSR_START_PAGE_FL&scname=CS_SSR_MANAGE_CLASSES_NAV&AJAXTransfer=y')
    time.sleep(3)

    #redirect to room selection page
    #driver.get("https://www.spire.umass.edu/psc/heproda_newwin/EMPLOYEE/SA/c/UM_H_SELF_SERVICE_FL.UM_H_SS_RMSELHM_FL.GBL?NavColl=true")

    #click on semester
    semester = driver.find_element(by=By.ID, value="SSR_ENTRMCUR_VW_ACAD_CAREER_DESCR$1")
    ActionChains(driver)\
        .click(semester)\
        .perform()
    time.sleep(3)

    #switch to add drop edit dropdown
    add_drop_edit_btn = driver.find_element(by=By.ID, value="SCC_LO_FL_WRK_SCC_VIEW_BTN$IMG$2")
    ActionChains(driver)\
        .click(add_drop_edit_btn)\
        .perform()
    time.sleep(3)

    #navigate to search add enroll button
    search_add_enroll_btn = driver.find_element(by=By.ID, value="win49divSCC_LO_FL_WRK_SCC_GROUP_BOX_1$21$$11")
    ActionChains(driver)\
        .click(search_add_enroll_btn)\
        .perform()
    time.sleep(3)

    #additional ways to search btn
    additional_ways_to_search_btn = driver.find_element(by=By.ID, value="SSR_CLSRCH_FLDS_PTS_ADV_SRCH")
    ActionChains(driver)\
        .click(additional_ways_to_search_btn)\
        .perform()
    time.sleep(3)


main()