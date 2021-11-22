from flask import Flask, redirect, url_for, render_template, request
from flask_mail import Mail, Message
from . import Connections


app = Flask(__name__)


# settings for sending email notifications - NOT FINAL VALUES
# (should be changed when switching to use a Kaiser domain email)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'RMSNotifications1@gmail.com'
app.config['MAIL_PASSWORD'] = 'Rm$aPp01'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

@app.route("/help")
def help_page():
    return render_template('help.html')


@app.route("/chocksMenu")
def chocksMenu():
    return render_template('chocksMenu.html')


@app.route("/chocksView")
def chocksView():
    headings = ("Roll ID", "Status", "Current Diameter", "Starting Diameter", "Mill", "Roll Type", "Manufacture Date")
    data, committed, message = Connections.query_results("Select *  FROM report ORDER BY date DESC", 7)
    if committed is True:
        return render_template('chocksView.html', headings=headings, data=data)
    else:
        return message #error message, needs an html page
    

@app.route("/chocks")
def chocks():
    return render_template('chocks.html')


@app.route("/notifications")
def notifications():
    send_notification_email(1001) # RELOCATE THIS TO SEND EMAIL WHEN REPLACEMENT SHOULD BE ORDERED
    return render_template('notifications.html')


@app.route("/")
def home():
    headings = ("Roll ID", "Status", "Current Diameter", "Starting Diameter", "Mill", "Roll Type", "Manufacture Date")
    data, committed, message = Connections.query_results("Select *  FROM roll ORDER BY roll_num DESC", 7)
    if committed is True:
        return render_template("index.html", headings=headings, data=data)
    else:
        return message #display error message, needs an html page



#Replace with /index when its finished
@app.route("/queryresults") #this will eventually replace home/index.html
def query():
    #return query_results()
    return render_template('rollData.html')#temporary link

#Add chock function
@app.route('/add-chock', methods = ['GET','POST'])
def add_chock():
    if request.method == 'POST':
        committed, message = Connections.add_chock(request)
        if (committed is True):
            return 'succesfully added chock' #maybe option to view all chocks forms after submitting
        else:
            return message #error message
    return 'thing'

@app.route('/add-email', methods = ['GET','POST'])#template for saving data from a webpage
def add_email():
    if request.method == 'POST':
        committed, message = Connections.add_email(request)
        if committed is True:
            return 'email succesfully added'
        else:
            return message #error message
    return 'thing'

@app.route('/remove-email', methods = ['POST'])
def remove_email():
    if request.method == 'POST':
        committed, message = Connections.remove_email(request)
        if committed is True:
            return 'email succesfully removed'
        else:
            return message #error message
    return 'thing'


def send_notification_email(roll_id):
    mail = Mail(app)
    message = Message('TEST MESSAGE', sender='RMSNotifications1@gmail.com')
    # NEED TO REFORMAT THIS WITH HTML - include something about the recipient being on
    # the notifications list and how to get off of it
    message.body = f'This email should say something about a new roll needing to be ordered\
    (and include the roll_num: {roll_id} that is being replaced)'
    # USING MY EMAIL FOR NOW - should add all recipients on notifications list
    message.add_recipient('rmsnotirecipient@gmail.com')
    mail.send(message)
    return 'Notification Email Sent'


if __name__ == "__main__":
    app.run()