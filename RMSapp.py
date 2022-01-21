from flask import Flask, redirect, url_for, render_template, request
from flask_mail import Mail, Message
import Connections
import Notifications as notif

app = Flask(__name__)
rms_mail = Mail(app)

RMS_EMAIL = 'RMSNotifications1@gmail.com' # change for Kaiser email
# settings for sending email notifications - NOT FINAL VALUES
# (should be changed when switching to use a Kaiser domain email)
app.config['MAIL_SERVER']='smtp.gmail.com' # change for Kaiser email
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] =  RMS_EMAIL
app.config['MAIL_PASSWORD'] = 'Rm$aPp01' # change for Kaiser email
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
    # send_notification_email(1001) # RELOCATE THIS TO SEND EMAIL WHEN REPLACEMENT SHOULD BE ORDERED
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

# function to send a notification email to the registered users in the RMS
def send_notification_email():
    # SAMPLE DATA TO TEST NOTI EMAIL RENDERING
    rolls_at_EOL = [[]]
    rolls_near_EOL = [[]]

    # get rolls at (or past) the end of their lifespan

    # get rolls near the end of their lifespan

    # get notification recipients from the RMS database
    recipients = []

    # send the notification email
    notif.send_noti_email(rolls_at_EOL, rolls_near_EOL, RMS_EMAIL, recipients, rms_mail)

    # OLD WAY OF SENDING NOTIFICATION EMAILS
    # mail = Mail(app)
    # message = Message('TEST MESSAGE', sender='RMSNotifications1@gmail.com')

    # # NEED TO REFORMAT THIS WITH HTML - include something about the recipient being on
    # # the notifications list and how to get off of it
    # # INFO TO INCLUDE IN THE EMAIL - 
    # message.body = f'This email should say something about a new roll needing to be ordered\
    # (and include the roll_num: {roll_id} that is being replaced)'

    # # ONLY WORKS WHEN CONNECTED TO KAISER NETWORK
    # try: # connect to RMS database REPLACE WITH Connections.py
    #     connection = pp.connect('Driver= {SQL Server};Server=localhost\\SQLEXPRESS;Database=rms;'
    # 'uid=rmsapp;pwd=ss1RMSpw@wb02') 
    #     cur = connection.cursor()
    # except pp.Error as e: # couldn't connect to 
    #     error_message = "error connecting to SQL Server: " + str(e) #returns error type
    #     return error_message

    # try: # query database to get emails we need to notify
    #     cur.execute('SELECT email FROM employee;')
    #     emails = cur.fetchall()
    #     for row in emails: # add emails to the message as recipients
    #         message.add_recipient(row[0])
    # except pp.Error as e: # the SQL query fails
    #     return 'error getting emails: ' + str(e)
    
    # # USING TEST EMAIL FOR NOW - should query database and add all registered recipients
    # # TEST EMAIL RECIPIENT CREDENTIALS - rmsnotirecipient@gmail.com / Rm$noT1s
    # message.add_recipient('rmsnotirecipient@gmail.com')
    # mail.send(message)

if __name__ == "__main__":
    app.run()