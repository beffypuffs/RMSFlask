# Test file to make sure data is properly queried from the RMS database
# Written by Joshua Seward
# Date Created - 3 February 2021
# Last Modified - 3 February 2021

import pytest
from Connections import sql_connect, rolls_order_now, rolls_order_soon, email_notification_recipients

# database connection
TEST_CONNECTION, CONNECTION_MESSAGE = sql_connect()

# correct data that should be retrieved by get_rolls_now()
GET_ROLLS_NOW_RESULTS = [['2326', '37.3', '37.0', '2022-02-23', 'None', '132', 'WORK'],
                         ['16049', '18.772', '18.6', '2022-04-19', 'None', 'CM', 'WORK'],
                         ['16050', '18.773', '18.6', '2022-04-19', 'None', 'CM', 'WORK'],
                         ['16043', '18.7462', '18.6', '2022-05-26', 'None', 'CM', 'WORK'],
                         ['16044', '18.745', '18.6', '2022-05-26', 'None', 'CM', 'WORK'],
                         ['1532', '23.277', '23.0', '2022-07-26', 'None', '80', 'IMR']]

# correct data that should be retrieved by get_rolls_soon()
GET_ROLLS_SOON_RESULTS = [['2327', '37.493', '37.0', '2023-03-06', 'None', '132', 'WORK'],
                         ['2328', '37.493', '37.0', '2023-03-06', 'None', '132', 'WORK']]

# correct data that should be retrieved by email_notification_recipients()
EMAIL_NOTIFICATION_RECIPIENTS_RESULTS = ['rmsnotirecipient@gmail.com']

def test_get_rolls_now():
    """Test the rolls_order_now() function to make sure the correct data is retrieved 
    from the sample database.
    """
    rolls_data, query_executed, message = rolls_order_now(connection=TEST_CONNECTION)
    assert query_executed
    assert rolls_data == GET_ROLLS_NOW_RESULTS

def test_get_rolls_soon():
    """Test the rolls_order_soon() function to make sure the correct data is retrieved 
    from the sample database.
    """
    rolls_data, query_executed, message = rolls_order_soon(connection=TEST_CONNECTION)
    assert query_executed
    assert rolls_data == GET_ROLLS_SOON_RESULTS

def test_email_notification_recipients():
    """Test the email_notification_recipients() function to make sure the correct data is 
    retrieved from the sample database
    """
    rolls_data, query_executed, message = email_notification_recipients(connection=TEST_CONNECTION)
    assert query_executed
    assert rolls_data == EMAIL_NOTIFICATION_RECIPIENTS_RESULTS