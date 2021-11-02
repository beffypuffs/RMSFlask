"""
Testing file for RMS Input Sanitation
Written By - Joshua Seward
"""
import InputSanitization as sanitization
import pytest

# check that a generic email from kaiser passes through sanitization
def email_test_1():
    assert sanitation.email_input_sanitation('exampleUser123@kaisertwd.com') == True