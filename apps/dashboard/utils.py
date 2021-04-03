import re

def contains_digit(string):
    RE_digit = re.compile('\d')
    return RE_digit.search(string)

def contains_uppercase(string):
    RE_upper = re.compile('[A-Z]')
    return RE_upper.search(string)

def is_valid_email(email):
    RE_EMAIL = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    return RE_EMAIL.match(email)

