"""
 driver.py
~~~~~~~~~
This is the module that runs the program.
"""

import jsonpickle
from selenium.common.exceptions import WebDriverException
from time import sleep


from cu_register.utils import determine_query
from cu_register.utils import update_config

from cu_register.webutils import init_driver
from cu_register.webutils import fetch_courses
from cu_register.webutils import check_courses
from cu_register.webutils import retry
from cu_register.webutils import login
from cu_register.webutils import register_course
from cu_register.webutils import check_credentials

from cu_register.io import create_user
from cu_register.io import create_courses
from cu_register.logging import logger

# global settings
HEADLESS_MODE = False  # run chrome in headless mode
WAIT_TIME = 5  # driver wait to find element
SCAN_FREQUENCY = 60  # how long to wait in seconds before each run
SLEEP_TIME = 600 # how long to sleep after error occurs
MAX_ERRORS = 5 # after how many errors should program exit

# start driver on start-up
init_driver(WAIT_TIME, HEADLESS_MODE)

# file handling
with open('config/config.json', 'r+') as f:
    # noinspection PyBroadException
    try:
        file = f.read()
        user, courses = jsonpickle.decode(file)
    except ValueError:
        user = create_user()
        courses = create_courses()
        logger.info("CHECKING CREDENTIALS")
        if check_credentials(user):
            logger.info("CREDENTIALS CONFIRMED")
        else:
            logger.error("CREDENTIALS FAILED\nEXITING")
            exit(1)
        # save data to file
        data = jsonpickle.encode([user, courses])
        f.write(data)

# find query to best search for courses
query = determine_query(courses=courses)
logger.error("SCANNING BEGUN")

# begin scanning
fetch_courses(query=query)
errors = 0
while True:
    try:
        course = check_courses(courses=courses)
        logger.info("SCANNED")
        if course:
            logger.error(f"COURSE FOUND: {course.subject} {course.course_number}" )
            login(user=user)
            result = register_course(course=course)
            if result:
                logger.error("SUCCESSFULLY REGISTERED FOR COURSE")
                courses.remove(course)
                update_config(user, courses)
            else:
                logger.error("COURSE REGISTRATION FAILED")
                exit(1)
        else:
            retry()
        sleep(SCAN_FREQUENCY)
    except (OSError, WebDriverException):
        errors = errors + 1
        if errors >= MAX_ERRORS:
            exit(1)
        logger.error('SCANNING TIMED OUT')
        sleep(SLEEP_TIME)