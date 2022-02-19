from flask import Flask, redirect, url_for, render_template, request, session
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import asc, desc
import Connections
import Requests
import History
import Notifications as notif
import pymssql
from flask_apscheduler import APScheduler
from logging import basicConfig, DEBUG, info, debug, error
from os import path


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
    SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://RMS:trpJ63iGY4F7mRj@rmssql.database.windows.net/RMSSQL'

app = Flask(__name__)
app.config.from_object(RMSConfig())
db = SQLAlchemy(app)


Base = automap_base() #Makes a class for all tables in the database
Base.prepare(db.engine, reflect = True)
Roll = Base.classes.roll_new
Grind = Base.classes.grind_new #what is displayed
Grinds = Base.classes.Grinds #closer to what the final grind class should look like
Info = Base.classes.roll_info



# results = db.session.query(Roll).order_by(Roll.approx_scrap_date)
# #results = db.session.query(info).all()
# for result in results:
#     print("thing:")
#     print(result.approx_scrap_date)


# initialize flask-mail
rms_mail = Mail(app)

# initialize scheduler
scheduler = APScheduler()
scheduler.init_app(app)

# initialize logging
RMS_LOGS_PATH = path.join('logs', 'RMSapp.log')
RMS_LOGS_FORMAT  = '%(asctime)s : %(levelname)s - %(message)s'
# basicConfig(filename=RMS_LOGS_PATH, format=RMS_LOGS_FORMAT, level=DEBUG)
# info('Starting RMSapp...')


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
                error('PROBLEM SENDING NOTIFICATION EMAIL - ' + message)
            order_soon, order_soon_committed, message = Connections.rolls_order_soon(connection)
            if not order_soon_committed:
                error('PROBLEM SENDING NOTIFICATION EMAIL - ' + message)
            recipients, recipients_committed, message = Connections.email_notification_recipients(connection)
            if not recipients_committed:
                error('PROBLEM SENDING NOTIFICATION EMAIL - ' + message)
            if recipients != [] and (order_now != [] or order_soon != []):
                notif.send_noti_email(order_now, order_soon, RMS_EMAIL, recipients, rms_mail)
                debug('Notification Email Sent')
            else:
                debug('Notification Email NOT SENT - No roll replacements to order')
        else:
            error('PROBLEM CONNECTING TO DATABASE - ' + conn_message)

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
    return render_template('notifications.html')


@app.route("/")
def home():
    #db.session.query(Grinds).delete()
    #History.translate_history(db, Grinds, 'grindFiles')
    headings = ("Roll ID", "Diameter", "Scrap Diameter", "Approx. Scrap Date", "Grinds Left", "Mill", "Roll Type")
    # if message == "connected":
    #     debug("Connected to RMS database")
    #     # data, committed, message = Connections.query_results(connection, "Select *  FROM roll_new ORDER BY approx_scrap_date ASC", 7)
    #     roll = db.Table('roll_new', db.metadata, autoload=True, autoload_with=db.engine)
    #     data = db.session.query(roll).all()
    #     if committed is True:
    #         debug('Home Page Loaded Successfully - ' + message)
    #         return render_template("index.html", headings=headings, data=data)
    #     else:
    #         error('PROBLEM LOADING HOME PAGE - ' + message)
    #         return render_template('error.html', message = message) #error message
    # else:
    #     error('PROBLEM CONNECTING TO RMS DATABASE - ' + message)
    #     return render_template('error.html', message = message) #error message
    # roll = db.Table('roll_new', db.metadata, autoload=True, autoload_with=db.engine)
    results = db.session.query(Roll).order_by(Roll.approx_scrap_date)
    # names = []
    # for c in Roll.__table__.columns:
    #     names.append(c.name)
    return render_template('index.html', headings=headings, data=results)


#Add chock function
@app.route('/add_chock', methods = ['GET','POST'])
def add_chock():
    connection, message = Connections.sql_connect()
    if request.method == 'POST':
        if (request.form['submitResponse'] == 'Submit Form'):
            data = Requests.chock_request_data(request)
            committed, message = Connections.add_chock(connection, data)
            if (committed is True):
                debug('Chocks & Bearings Form ADDED successfully')
                return render_template('successfulAdd.html') #maybe option to view all chocks forms after submitting
            else:
                error('Problem ADDING Chocks & Bearings Form' + message)
                return render_template('error.html', message = message) #error message
        elif (request.form['submitResponse'] == 'Remove Form'):
            data = Requests.chock_request_data(request)
            committed, message = Connections.remove_chock(connection, data)
            if (committed is True):
                debug('Chocks & Bearings Form REMOVED successfully')
                return render_template('successfulRemove.html')
            else:
                error('Problem REMOVING Chocks & Bearings Form' + message)
                return render_template('error.html', message = message) #error message
        else:
            data = Requests.chock_request_data(request)
            committed, message = Connections.edit_chock(connection, data)
            if (committed is True):
                debug('Chocks & Bearings Form EDITED successfully')
                return render_template('successfulEdit.html')
            else:
                error('Problem EDITING Chocks & Bearings Form' + message)
                return render_template('error.html', message = message) #error message

@app.route('/add-email', methods = ['GET','POST'])#template for saving data from a webpage
def add_email():
    if request.method == 'POST':
        connection = Connections.sql_connect()
        data = Requests.email_request_data(request)
        committed, message = Connections.add_email(connection, data)
        if committed is True:
            debug('Email succesfully ADDED')
        else:
            error('Problem ADDING email - ' + message)
            return render_template('error.html', message = message) #error message

@app.route('/remove-email', methods = ['POST'])
def remove_email():
    if request.method == 'POST':
        connection = Connections.sql_connect()
        data = Requests.email_request_data(request)
        committed, message = Connections.remove_email(connection, data)
        if committed is True:
            debug('Email succesfully REMOVED')
        else:
            error('Problem REMOVING email - ' + message)
            return render_template('error.html', message = message) #error message
    return 'thing'

@app.route('/roll-view', methods = ['POST'])
def roll_view():
    if request.method == 'POST':
        roll_num = request.form['roll_clicked']
        # connection, message = Connections.sql_connect()
        # cur = connection.cursor()
        # cur.execute(f'SELECT * FROM grind_new WHERE roll_num = {roll_num} ORDER BY min_diameter ASC')
        roll = db.session.query(Roll).filter_by(roll_num=roll_num).first() #since we know this is only going to grab 1 result, we just grab the first item in the initial resulting list. Result is a roll object 
        grinds = db.session.query(Grinds).filter_by(roll_num=roll_num).order_by(Grinds.entry_time) #returns list of all grinds 
        info = db.session.query(Info).filter_by(mill=roll.mill, roll_type=roll.roll_type).first() #Returns the first item in the list, 
        graph = Connections.generate_graphs(roll, grinds, info)
        return render_template('rollView.html', graph=graph, roll_num = roll_num, last_grinds=grinds, num_grinds=grinds.count())


# def send_status_report():
#     mail = Mail(app)
#     #send current diameter and projected lifespan of each roll
# History.make_data(db, Roll, Grinds, Info)
#rolls = db.session.query(Roll).all()

#Connections.update_scrap_date(db, Roll, Grinds, Info)

if __name__ == "__main__":
    app.run()