"""
models.py
~~~~~~~~~
This module provides objects that power this project.
"""
from dataclasses import dataclass


@dataclass
class Course:
    """ represents course """
    term: str
    subject: str
    course_number: str


@dataclass
class User:
    """ represents user """

    username: str
    password: str
    duo_passcodes: list

    def get_passcode(self) -> str:
        return self.duo_passcodes.pop()
