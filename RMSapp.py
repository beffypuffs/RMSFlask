from flask import Flask, redirect, url_for, render_template, request, g
from flask_mail import Mail, Message
import Connections
import Requests
import Notifications as notif
from flask_apscheduler import APScheduler

# settings for sending email notifications - NOT FINAL VALUES
# (should be changed when switching to use a Kaiser domain email)
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
def send_notification_email():
    """Sends a notification email using flask-mail. Move to within the RMSApp 
    Flask context. Connect to the database and check the connection. Query the 
    RMS database for the rolls that need to be reordered immediately (less 
    than a year from now) and the rolls that need to be reordered within the 
    next 3 months (12-15 months from now). Query the database for recipients 
    of the notification emails. Chek if there is any notification data to send 
    and if there are any recipients. Send a notification email if there one 
    needs to be sent.
    """
    with scheduler.app.app_context():
        connection, conn_message = Connections.sql_connect()
        if conn_message == "connected":
            order_now, order_now_committed, message = Connections.rolls_order_now(connection)
            if not order_now_committed:
                return message
            order_soon, order_soon_committed, message = Connections.rolls_order_soon(connection)
            if not order_soon_committed:
                return message
            recipients, recipients_committed, message = Connections.email_notification_recipients(connection)
            if not recipients_committed:
                return message
            if recipients != [] and (order_now != [] or order_soon != []):
                notif.send_noti_email(order_now, order_soon, RMS_EMAIL, recipients, rms_mail)
        else:
            return conn_message # CHANGE TO A LOGGING STATEMENT

# begin the scheduler to send notification emails
scheduler.start()

@app.route("/help")
def help_page():
    return render_template('help.html')


@app.route("/chocksMenu")
def chocksMenu():
    return render_template('chocksMenu.html')


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
            return render_template('error.html', message = message) #error message
    else:
        connection, message = Connections.sql_connect()
        data, committed, message = Connections.query_results(connection, "Select *  FROM report ORDER BY date DESC", 54)
        if committed is True:
            return render_template('chocksView2.html', data = data, i = 0, length = len(data)) #see above
        else:
            return render_template('error.html', message = message) #error message


@app.route("/chocks")
def chocks():
    return render_template('chocks.html')


@app.route("/notifications")
def notifications():
    # send_notification_email(1001) # RELOCATE THIS TO SEND EMAIL WHEN REPLACEMENT SHOULD BE ORDERED
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
            return render_template('error.html', message = message) #error message
    else:
        return render_template('error.html', message = message) #error message



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
                return render_template('error.html', message = message) #error message
        elif (request.form['submitResponse'] == 'Remove Form'):
            data = Requests.chock_request_data(request)
            committed, message = Connections.remove_chock(connection, data)
            if (committed is True):
                return render_template('successfulRemove.html')
            else:
                return render_template('error.html', message = message) #error message
        else:
            data = Requests.chock_request_data(request)
            committed, message = Connections.edit_chock(connection, data)
            if (committed is True):
                return render_template('successfulEdit.html')
            else:
                return render_template('error.html', message = message) #error message

@app.route('/add-email', methods = ['GET','POST'])#template for saving data from a webpage
def add_email():
    if request.method == 'POST':
        connection = Connections.sql_connect()
        data = Requests.email_request_data(request)
        committed, message = Connections.add_email(connection, data)
        if committed is True:
            return 'email succesfully added'
        else:
            return render_template('error.html', message = message) #error message
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
            return render_template('error.html', message = message) #error message
    return 'thing'

@app.route('/roll-view', methods = ['POST'])
def roll_view():
    if request.method == 'POST':
        roll_num = request.form['roll_clicked']
        connection, message = Connections.sql_connect()
        cur = connection.cursor()
        cur.execute(f'SELECT * FROM grind_new WHERE roll_num = {roll_num} ORDER BY min_diameter ASC')
        last_grinds = cur.fetchall()
        Connections.generate_graphs(roll_num)
        return render_template('rollView.html', graph=Connections.generate_graphs, roll_num = roll_num, last_grinds=last_grinds, num_grinds=len(last_grinds))

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

# def send_status_report():
#     mail = Mail(app)
#     #send current diameter and projected lifespan of each roll


# @app.before_request
# def set_db():
#     if not hasattr(g, 'sqllite_db'):
#         g.sqlite_db = Connections.sql_connect()
#     return g.sqlite_db


if __name__ == "__main__":
    app.run()