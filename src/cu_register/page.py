"""
page.py
~~~~~~~
This module provides pages classes for data encapsulation.
"""
from dataclasses import dataclass
import requests


@dataclass
class TermSelectionPage:
    url = 'https://regssb.sis.clemson.edu/StudentRegistrationSsb/ssb/term/termSelection?mode=search'
    terms_url = 'https://regssb.sis.clemson.edu/StudentRegistrationSsb/ssb/classSearch/getTerms?dataType=json&searchTerm=&offset=1&max=10'
    term_dropdown = '#s2id_txt_term'
    submit = '#term-go'

    @staticmethod
    def get_terms() -> list:
        terms = requests.get(TermSelectionPage.terms_url).json()
        terms = list(filter(lambda p: len(p.get('description')) < 12, terms))
        return terms



@dataclass
class CourseSearchPage:
    subject_field = '#s2id_txt_subject'
    subject_field_input = '.select2-input'
    course_number_input = '#txt_courseNumber'
    submit = '#search-go'


@dataclass
class CourseResultsPage:
    url = 'https://regssb.sis.clemson.edu/StudentRegistrationSsb/ssb/searchResults/searchResults?pageMaxSize=10000'
    add_section = '.add-section-button'
    save = '#saveButton'
    search_again = '#search-again-button'
    notification = ".notification-item"


@dataclass
class RegistrationPage:
    url = 'https://regssb.sis.clemson.edu/StudentRegistrationSsb/ssb/registration/registration'
    register = '#registerLink'


@dataclass
class LoginPage:
    username_field = '#username'
    password_field = '#password'
    submit = '#submitButton'
    duo_frame = '#duo_iframe'
    cancel = '.btn-cancel'
    use_passcodes = '.passcode-label'
    passcode_field = '[name="passcode"]'
    log_in = "#passcode"
