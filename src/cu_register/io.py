"""
io.py
~~~~~
This module handles all input validation as well as pretty
formatting (colors!).
"""
from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator
from prompt_toolkit.validation import ValidationError
from colored import fg, attr

from .models import Course
from .models import User

from .page import TermSelectionPage


# global color scheme
class Colors:
    sandstone = fg('#EFDBB2')
    tangerine = fg('#F56600')
    brick = fg("yellow")
    bold = attr('bold')
    blink = attr('blink')
    reset = attr('reset')


def multiline_input(string, validator, terminator=''):
    """ allows for multiline inputs """
    print(string)
    r = []
    while True:
        text = prompt('', validator=validator)
        if text == terminator:
            break
        r.append(text)
    return r


# validation classes are provided to minimize run-time errors
# caused by improper formatting

class PinValidator(Validator):
    """ validates Duo Passcodes """

    def validate(self, text):
        text: str = text.text

        is_required_length = len(text) == 7
        is_numeric = text.isnumeric()
        is_blank = text.strip() == ""

        if is_required_length and is_numeric:
            return
        elif is_blank:
            return

        raise ValidationError(message="Invalid Pin")


class CourseValidator(Validator):
    """ validates courses """

    def validate(self, text):
        text: str = text.text
        if not text:
            return
        try:
            subject, number = text.split()
            if len(subject) == 4 and subject.isalpha():
                pass
            if len(number) == 4 and number.isnumeric():
                return
        except ValueError:
            pass
        raise ValidationError(message="Invalid Course")


class TermValidator(Validator):
    """ validate term """
    term_data = TermSelectionPage.get_terms()
    terms = list(map(lambda t: t.get('description').upper(), term_data))

    def validate(self, text):
        text: str = text.text
        if text.upper() in self.terms:
            return

        raise ValidationError(message="Term must be " + " or ".join(self.terms))


def create_user():
    """ asks for input and creates User object """
    username = input("%sEnter your iRoar Username:%s\n" % (Colors.sandstone, Colors.reset))
    print("%sEnter your iRoar Password:%s" % (Colors.sandstone, Colors.reset))
    password = prompt("", is_password=True)
    passcodes = multiline_input(
        "%sEnter Duo passcodes (enter twice to finish):%s" % (Colors.sandstone, Colors.reset),
        validator=PinValidator())
    user = User(username, password, passcodes)
    return user


def create_courses():
    """ asks for input and creates list of courses """
    print("%sEnter the term you wish to register for:%s" % (Colors.sandstone, Colors.reset))
    term = prompt('', validator=TermValidator())
    for t in TermValidator.term_data:
        if term.capitalize() == t.get('description'):
            term = t.get('code')
    courses = multiline_input(
        "%sEnter a course on each line (enter twice to finish):%s" % (Colors.sandstone, Colors.reset),
        validator=CourseValidator())
    courses = [Course(term, *course.upper().split()) for course in courses]
    return courses
