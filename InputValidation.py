"""
Python file to provide input sanitation for the Kaiser RMS
Written By - Joshua Seward
"""
import re # library to use regexes

# input validation that checks for valid Kaiser email domains
def domain_validation(domain):
    # check the given domain against valid kaiser email domains
    domain_match = re.match("^@(kaisertwd.com|KaiserTWD.com)$", domain)
    return bool(domain_match)

# input validation that checks for valid email usernames
def username_validation(username):
    # check the given username against the valid characters for an email username
    username_match = re.match("^([a-z]|[A-Z]|[0-9])*$", username)
    return bool(username_match)
