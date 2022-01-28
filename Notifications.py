# File for sending notification emails as a part of the RMS system
# Author: Joshua Seward
# Date Created: 13 January 2022
# Last Modified: 13 January 2022

from flask import render_template
from flask_mail import Message

# method to send a notification email using a rendered HTML template
def send_noti_email(order_now, order_soon, sender, recipients, 
    mail):
    subject = 'RMS Roll Status Notification'

    # create the message using the given sender and recipients
    message = Message(subject=subject, recipients=recipients, 
    sender=sender)

    # headings for the roll grind data table in the HTML template
    headings = ("Roll ID", "Current Diameter", "Scrap Diameter", 
    "Approx Scrap Date", "Grinds Remaining", "Mill", "Roll Type")
    # render the HTML template using the given rolls
    message.html = render_template("noti_email.html", headings=headings, 
    order_now=order_now, order_soon=order_soon)

    # send notification email
    mail.send(message)