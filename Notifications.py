# File for sending notification emails as a part of the RMS system
# Author: Joshua Seward
# Date Created: 13 January 2022
# Last Modified: 13 January 2022

from flask import render_template
from flask_mail import Message

# method to send a notification email using a rendered HTML template
def send_noti_email(rolls_at_EOL, rolls_near_EOL, sender, recipients, mail):
    subject = 'RMS Roll Grind Notification'
    # create the message using the given sender and recipients
    message = Message(subject=subject, recipients=recipients, sender=sender)

    # render the HTML template using the given rolls and correct headings
    headings = ()

    # send notification email
    mail.send(message)