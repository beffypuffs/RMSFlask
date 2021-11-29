"""
Python file to send notifications as a part of the RMS app
Written By - Joshua Seward
"""

from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

# flask mail configurations
RMS_EMAIL = 'RMSNotifications1@gmail.com' # change for Kaiser email
# settings for sending email notifications
# (should be changed when switching to use a Kaiser domain email)
app.config['MAIL_SERVER']='smtp.gmail.com' # change for Kaiser email
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] =  RMS_EMAIL
app.config['MAIL_PASSWORD'] = 'Rm$aPp01' # change for Kaiser email
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# function to send a notification email to the registered users in the RMS
def send_notification_email(roll_id):
    mail = Mail(app)
    message = Message('TEST MESSAGE', sender='RMSNotifications1@gmail.com')

    # NEED TO REFORMAT THIS WITH HTML - include something about the recipient being on
    # the notifications list and how to get off of it
    # INFO TO INCLUDE IN THE EMAIL - 
    message.body = f'This email should say something about a new roll needing to be ordered\
    (and include the roll_num: {roll_id} that is being replaced)'

    # ONLY WORKS WHEN CONNECTED TO KAISER NETWORK
    # try: # connect to RMS database
    #     connection = pp.connect('Driver= {SQL Server};Server=localhost\\SQLEXPRESS;Database=rms;'
    # 'uid=rmsapp;pwd=ss1RMSpw@wb02') 
    #     cur = connection.cursor()
    #     try: # query database to get emails we need to notify
    #         cur.execute('SELECT email FROM employee;')
    #         emails = cur.fetchall()
    #         for row in emails: # add emails to the message as recipients
    #             message.add_recipient(row[0])
    #     except pp.Error as e: # the SQL query fails
    #         return 'error getting emails: ' + str(e)
    # except pp.Error as e: # couldn't connect to 
    #     error_message = "error connecting to SQL Server: " + str(e) #returns error type
    #     return error_message
    
    # USING TEST EMAIL FOR NOW - should query database and add all registered recipients
    message.add_recipient('rmsnotirecipient@gmail.com')
    mail.send(message)
    return 'Notification Email Sent'
