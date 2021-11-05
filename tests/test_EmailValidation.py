"""
Testing file for RMS Email Validation
Written By - Joshua Seward
"""
from re import T
from typing import ValuesView
import EmailValidation as validation

# check that a generic kaiser domain passes (lowercase)
def test_valid_email_domain_1():
    valid_email_domain = '@kaisertwd.com'
    assert validation.domain_validation(valid_email_domain) == True

# check that a generic kaiser domain passes (PascalCase)
def test_valid_email_domain_2():
    valid_email_domain = '@KaiserTWD.com'
    assert validation.domain_validation(valid_email_domain) == True
    
# check that a domain without the '@' character fails
def test_invalid_email_domain_1():
    invalid_email_domain = 'kaisertwd.com'
    assert validation.domain_validation(invalid_email_domain) == False
    
# check that a domain ending with an invalid character fails
def test_invalid_email_domain_2():
    invalid_email_domain = '@kaisertwd.com\''
    assert validation.domain_validation(invalid_email_domain) == False

# check that a domain starting with an invalid character fails
def test_invalid_email_domain_3():
    invalid_email_domain = '\\@kaisertwd.com'
    assert validation.domain_validation(invalid_email_domain) == False

# check that a domain including an invalid character fails
def test_invalid_email_domain_4():
    invalid_email_domain = 'Kaiser$TWD.com'
    assert validation.domain_validation(invalid_email_domain) == False

# check that a valid kaiser username passes (lastname)
def test_valid_email_username_1():
    valid_email_username = 'lastname'
    assert validation.username_validation(valid_email_username) == True

# check that a valid outside vendor username passes (ov#####)
def test_valid_email_username_2():
    valid_email_username = 'ov12345'
    assert validation.username_validation(valid_email_username) == True

# check that a username beginning with an invalid character fails
def test_invalid_email_username_1():
    invalid_email_username = '\'lastname'
    assert validation.username_validation(invalid_email_username) == False

# check that a username ending with an invalid character fails
def test_invalid_email_username_2():
    invalid_email_username = 'lastname\\'
    assert validation.username_validation(invalid_email_username) == False
    
# check that a username that includes an invalid character fails
def test_invalid_email_username_3():
    invalid_email_username = 'last$name'
    assert validation.username_validation(invalid_email_username) == False