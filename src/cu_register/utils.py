"""
utils.py
~~~~~~~~
This module provides utility functions that are used within this
project.
"""

from functools import reduce
import jsonpickle

from .models import Course


def determine_query(courses: [Course]):
    """ determines the optimal query to search for all requested
    courses """

    term = courses[0].term

    if len(set([c.subject for c in courses])) != 1:
        return Course(term, '', '')

    f = lambda a, b: ''.join([i if i == j else '%' for i, j in zip(a, b)])
    course_number = reduce(f, [c.course_number for c in courses])
    return Course(term, courses[0].subject, course_number)

def update_config(user, courses):
    """ updates configuration after passcode is used """
    with open("../config.json", "r+") as f:
        data = jsonpickle.encode([user, courses])
        f.write(data)