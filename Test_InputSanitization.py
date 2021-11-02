"""
Testing file for RMS Input Sanitation
Written By - Joshua Seward
"""
import InputSanitization as sanitization
import pytest

VALID_EMAIL_FORMAT_1 = 'exampleUser123@kaisertwd.com'
VALID_EMAIL_FORMAT_2 = 'ExampleUser456@KaiserTWD.com'
INVALID_EMAIL_FORMAT_1 = '\'inva\\i;dem$@i)@kaisertwd.com'

# check that a generic email from kaiser passes through sanitization
def email_test_1():
    assert sanitization.email_input_sanitization(VALID_EMAIL_FORMAT_1) == True