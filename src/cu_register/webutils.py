"""
webutils.py
~~~~~~~~~~~
This module provides all the web searching functionality.
"""

from time import sleep
import requests
import urllib3

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from .models import Course
from .models import User

from .page import TermSelectionPage
from .page import CourseSearchPage
from .page import CourseResultsPage
from .page import RegistrationPage
from .page import LoginPage


# disable insecure requests warning
urllib3.disable_warnings()

# helper functions
find = lambda e: driver.find_element_by_css_selector(e)
send_keys = lambda e, keys: find(e).send_keys(keys)
click = lambda e: find(e).click()


def init_driver(wait_time, headless=False):
    """ initializes webdriver with options """
    # driver options
    options = Options()
    if headless:
        options.add_argument('--headless')

    global driver
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(wait_time)


def fetch_courses(query: Course, fetch_mode=True):
    """ selects term, course subject, and course number """
    # load .page
    if fetch_mode:
        driver.get(TermSelectionPage.url)

    # enter course term
    click(TermSelectionPage.term_dropdown)
    click(f'[id="{query.term}"]')
    click(TermSelectionPage.submit)

    # enter course subject and course number
    click(CourseSearchPage.subject_field)
    send_keys(CourseSearchPage.subject_field_input, query.subject)
    click('#' + query.subject)
    send_keys(CourseSearchPage.course_number_input, query.course_number)
    click(CourseSearchPage.submit)


def check_courses(courses: [Course]):
    """ checks to see if any courses are open """
    # get json data for course results
    cookies = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}
    r = requests.get(CourseResultsPage.url, verify=False, cookies=cookies).json()

    # check if courses have seat open
    for i in courses:
        for j in r['data']:
            if j['seatsAvailable'] > 0:
                if j['subject'] == i.subject:
                    if j['courseNumber'] == i.course_number:
                        return i


def retry():
    """ retries course search """
    click(CourseResultsPage.search_again)
    click(CourseSearchPage.submit)


def login(user: User, auth=False):
    """ logs in to Banner and performs duo authentication """
    # load .page
    driver.get(RegistrationPage.url)
    click(RegistrationPage.register)

    # login
    send_keys(LoginPage.username_field, user.username)
    send_keys(LoginPage.password_field, user.password)
    click(LoginPage.submit)

    if auth: # if only in authentation mode, do not enter passcodes
        return

    # enter duo passcodes
    e = find(LoginPage.duo_frame)
    driver.switch_to.frame(e)
    sleep(1)  # prevent robot detection
    click(LoginPage.cancel)
    sleep(1)  # prevent robot detection
    click(LoginPage.use_passcodes)
    send_keys(LoginPage.passcode_field, user.get_passcode())
    click(LoginPage.log_in)
    driver.switch_to.default_content()

def check_credentials(user):
    try:
        login(user, auth=True)
    except NoSuchElementException:
        return False
    return True

def register_course(course: Course):
    """ finds and registers for course """
    fetch_courses(course, fetch_mode=False)
    click(CourseResultsPage.add_section)
    click(CourseResultsPage.save)
    try:
        click(CourseResultsPage.save)  # just for safety
    except UnexpectedAlertPresentException:
        return False
    return True

