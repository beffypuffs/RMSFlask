from flask import Flask, redirect, url_for, render_template, request
from flask_mail import Mail
from flask_apscheduler import APScheduler
import Connections
import Requests
import Notifications as notif

RMS_EMAIL = 'RMSNotifications1@gmail.com' # change for Kaiser email

class RMSConfig():
    """Class for Flask configuration (needed to send scheduled 
    notification emails)
    """
    # Flask-mail config settings - NOT FINAL VALUES
    MAIL_SERVER = 'smtp.gmail.com' # change for Kaiser email
    MAIL_PORT = 465
    MAIL_USERNAME = RMS_EMAIL
    MAIL_PASSWORD = 'Rm$aPp01'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    # Flask-APScheduler config settings
    SCHEDULER_API_ENABLED = True

app = Flask(__name__)
app.config.from_object(RMSConfig())

# initialize flask-mail
rms_mail = Mail(app)

# initialize scheduler
scheduler = APScheduler()
scheduler.init_app(app)

@scheduler.task('cron', id='send_notification_email', week='*', day_of_week='*')
# @scheduler.task('interval', id='send_notification_email', seconds=30, misfire_grace_time=10)
def send_notification_email():
    with scheduler.app.app_context():
        # function to send a notification email to registered users in the RMS
        # create a connection w/ the database
        connection, conn_message = Connections.sql_connect()

        if conn_message == "connected":
            # get rolls to order IMMEDIATELY (1 year in advance) 
            order_now, order_now_committed, message = Connections.rolls_order_now(connection)
            if not order_now_committed:
                return message
            # get rolls to order SOON (15 months in advance)
            order_soon, order_soon_committed, message = Connections.rolls_order_soon(connection)
            if not order_soon_committed:
                return message
            # get notification recipients from the RMS database
            recipients, recipients_committed, message = Connections.email_notification_recipients(connection)
            if not recipients_committed:
                return message
            notif.send_noti_email(order_now, order_soon, RMS_EMAIL, recipients, rms_mail)
            print('Email Sent')
        else:
            return conn_message

scheduler.start()

@app.route("/help")
def help_page():
    send_notification_email() # RELOCATE THIS TO SEND EMAIL WHEN REPLACEMENT SHOULD BE ORDERED
    return render_template('help.html')


@app.route("/chocksMenu")
def chocksMenu():
    return render_template('chocks.html')


@app.route("/chocksView", methods = ['GET','POST']) 
def chocksView():
    if request.method == 'POST':
        i = int(request.form['form_num'])
        next_or_prev = request.form['submitResponse']
        if next_or_prev == "Next form":
            i -= 1
        else:
            i += 1
        connection, message = Connections.sql_connect()
        data, committed, message = Connections.query_results(connection, "Select *  FROM report ORDER BY date DESC", 54)
        if committed is True:
                return render_template('chocksview2.html', data = data, i = i, length = len(data)) #right now it sends every form which i'll fix later
        else:
            return message
    else:
        connection, message = Connections.sql_connect()
        data, committed, message = Connections.query_results(connection, "Select *  FROM report ORDER BY date DESC", 54)
        if committed is True:
            return render_template('chocksView2.html', data = data, i = 0, length = len(data)) #see above
        else:
            return message #error message, needs an html page


@app.route("/chocks")
def chocks():
    return render_template('chocks.html')


@app.route("/notifications")
def notifications():
    return render_template('notifications.html')


@app.route("/")
def home():
    headings = ("Roll ID", "Diameter", "Scrap Diameter", "Approx. Scrap Date", "Grinds Left", "Mill", "Roll Type")
    connection, message = Connections.sql_connect()
    if message == "connected":
        data, committed, message = Connections.query_results(connection, "Select *  FROM roll_new ORDER BY approx_scrap_date ASC", 7)
        if committed is True:
            return render_template("index.html", headings=headings, data=data)
        else:
            return message #display error message, needs an html page
    else:
        return message



#Replace with /index when its finished
@app.route("/queryresults") #this will eventually replace home/index.html
def query():
    #return query_results()
    return render_template('rollData.html')#temporary link

#Add chock function
@app.route('/add_chock', methods = ['GET','POST'])
def add_chock():
    connection, message = Connections.sql_connect()
    if request.method == 'POST':
        if (request.form['submitResponse'] == 'Submit Form'):
            data = Requests.chock_request_data(request)
            committed, message = Connections.add_chock(connection, data)
            if (committed is True):
                return render_template('successfulAdd.html') #maybe option to view all chocks forms after submitting
            else:
                return message #error message
        elif (request.form['submitResponse'] == 'Remove Form'):
            data = Requests.chock_request_data(request)
            committed, message = Connections.remove_chock(connection, data)
            if (committed is True):
                return render_template('successfulRemove.html')
            else:
                return message
        else:
            data = Requests.chock_request_data(request)
            committed, message = Connections.edit_chock(connection, data)
            if (committed is True):
                return render_template('successfulEdit.html')
            else:
                return message

@app.route('/add-email', methods = ['GET','POST'])#template for saving data from a webpage
def add_email():
    if request.method == 'POST':
        connection = Connections.sql_connect()
        data = Requests.email_request_data(request)
        committed, message = Connections.add_email(connection, data)
        if committed is True:
            return 'email succesfully added'
        else:
            return message #error message
    return 'thing'

@app.route('/remove-email', methods = ['POST'])
def remove_email():
    if request.method == 'POST':
        connection = Connections.sql_connect()
        data = Requests.email_request_data(request)
        committed, message = Connections.remove_email(connection, data)
        if committed is True:
            return 'email succesfully removed'
        else:
            return message #error message
    return 'thing'

@app.route('/roll-view', methods = ['POST'])
def roll_view():
    if request.method == 'POST':
        roll_num = request.form['roll_clicked']
        Connections.generate_graphs(roll_num)
        return render_template('rollView.html', graph=Connections.generate_graphs, roll_num = roll_num)

if __name__ == "__main__":
    app.run()