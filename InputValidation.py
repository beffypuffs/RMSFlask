"""
Python file to provide input sanitation for the Kaiser RMS
Written By - Joshua Seward
"""
import re # library to use regexes

# input validation that checks for valid Kaiser email domains
def domain_validation(domain):
    domain_match = re.match("@kaisertwd.com", domain, re.I)
    return bool(domain_match)
