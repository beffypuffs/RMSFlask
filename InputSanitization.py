"""
Python file to provide input sanitation for the Kaiser RMS
Written By - Joshua Seward
"""
import re

# input sanitation for adding emails to the notifications list
def email_input_sanitation(email):
    accepted_email_chars = re.compile('[a-zA-Z0-9]*@kaisertwd.com')
    return accepted_email_chars.match(email)