# File for sending notification emails as a part of the RMS system
# Author: Joshua Seward
# Date Created: 13 January 2022
# Last Modified: 1 February 2022

from flask import render_template
from flask_mail import Message

# subject for the RMS email notification
SUBJECT = 'RMS Roll Status Notification'

# headings for the roll grind data table in the HTML template
HEADINGS = ("Roll ID", "Current Diameter", "Scrap Diameter", 
"Approx Scrap Date", "Grinds Remaining", "Mill", "Roll Type")

def send_noti_email(order_now, order_soon, sender, recipients, mail):
    """Creates and sends a notification email using given data. 
    Creates a message from the constant subject, the given list of 
    recipients, and the given sender. Render the noti_email.html 
    template using the constant headings, and the given lists of rolls 
    to order now and soon. Then send the notification email using 
    flask-mail.
    """
    message = Message(subject=SUBJECT, recipients=recipients, 
    sender=sender)
    message.html = render_template("noti_email.html", headings=HEADINGS, 
    order_now=order_now, order_soon=order_soon)
    mail.send(message)