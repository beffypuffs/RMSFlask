"""
Testing file for RMS Input Sanitation
Written By - Joshua Seward
"""
from re import T
from typing import ValuesView
import InputValidation as validation

# check that a generic email from kaiser passes through sanitization
def test_valid_email_domain_1():
    valid_email_domain = '@kaisertwd.com'
    assert validation.domain_validation(valid_email_domain) == True

def test_valid_email_domain_2():
    valid_email_domain = '@KaiserTWD.com'
    assert validation.domain_validation(valid_email_domain) == True
