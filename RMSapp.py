from flask import Flask, redirect, url_for, render_template, request, session
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
import sqlalchemy as sa
from models import * 
from datetime import timedelta
import Connections
import Requests
import History
import random
import Notifications as notif
import pymssql
#import pyodbc
from flask_apscheduler import APScheduler
from logging import basicConfig, DEBUG, info, debug, error
from os import path


# settings for sending email notifications - NOT FINAL VALUES
# (should be changed when switching to use a Kaiser domain email)
RMS_EMAIL = 'RMSNotifications1@gmail.com' # change for Kaiser email
CUR_DAY = datetime.datetime.now() - datetime.timedelta(weeks=52)

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
    # USERNAME = 'RMS'
    # PWD = 'trpJ63iGY4F7mRj'
    # HOST = 'rmssql.database.windows.net'
    # DB = 'RMSSQL'
    # DRIVER = 'ODBC Driver 17 for SQL Server'

    # SQLALCHEMY_DATABASE_URI = sa.engine.url.URL(
    #     "mssql+pyodbc",username=USERNAME,password=PWD, host=HOST, database=DB,
    #     query={"driver": DRIVER}
    # )


app = Flask(__name__)
app.config.from_object(RMSConfig())
db = SQLAlchemy(app)


# initialize flask-mail
rms_mail = Mail(app)

# initialize scheduler
scheduler = APScheduler()
scheduler.init_app(app)
# scheduler.add_job(func=process_new_files, trigger="interval", minutes = 60)

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

@app.route("/add_roll", methods = ["POST"])
def add_roll():
    if request.method == "POST":
        roll_num = request.form['roll_SN']
        start_diameter = request.form['start_diameter']
        roll_type = request.form['roll_type']
        mill = request.form['mill']
        info = db.session.query(Info).filter_by(mill=mill, roll_type=roll_type)[0]
        newRoll = Roll(roll_num=roll_num, diameter = start_diameter, scrap_diameter=info.scrap_diameter, mill=mill, roll_type=roll_type, num_grinds=0, scrapped=False)
        db.session.add(newRoll)
        db.session.commit()
        return render_template('successfulRollAdd.html')
    else:
        return "How"


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
        reports = db.session.query(Report).order_by(Report.date.desc()).all()
        return render_template('chocksview2.html', data = reports[i], i = i, length = len(reports))
    else:
        reports = db.session.query(Report).order_by(Report.date.desc()).all()
        return render_template('chocksView2.html', data = reports[0], i = 0, length = len(reports))


@app.route("/chocks", methods = ['GET', 'POST'])
def chocks():
    if request.method == 'GET':
        return render_template('chocks.html')
    elif request.method == 'POST':
        return 'POST'


@app.route("/notifications")
def notifications():
    return render_template('notifications.html')


@app.route("/")
def home():
    # reset_stats()
    # global CUR_DAY
    # advance_one_year(CUR_DAY)
    # CUR_DAY = CUR_DAY + datetime.timedelta(weeks=52) ##this is just for demo purposes, wont be used in production
    headings = ("Roll ID", "Diameter", "Scrap Diameter", "Approx. Scrap Date", "Grinds Left", "Mill", "Roll Type")
    results = db.session.query(Roll).order_by(Roll.approx_scrap_date)

    return render_template('index.html', headings=headings, data=results)


#Add chock function
@app.route('/add_chock', methods = ['GET','POST'])
def add_chock():
    if request.method == 'POST':
        if (request.form['submitResponse'] == 'Submit Form'):
            data = Requests.chock_request_data(request)
            committed, message = Connections.add_chock(data, Report)
            if (committed is True):
                debug('Chocks & Bearings Form ADDED successfully')
                return render_template('successfulAdd.html') #maybe option to view all chocks forms after submitting
            else:
                error('Problem ADDING Chocks & Bearings Form' + message)
                return render_template('error.html', message = message) #error message
        elif (request.form['submitResponse'] == 'Remove Form'):
            data = Requests.chock_request_data(request)
            committed, message = Connections.remove_chock(data)
            if (committed is True):
                debug('Chocks & Bearings Form REMOVED successfully')
                return render_template('successfulRemove.html')
            else:
                error('Problem REMOVING Chocks & Bearings Form' + message)
                return render_template('error.html', message = message) #error message
        else:
            data = Requests.chock_request_data(request)
            i = request.form['form_num']
            committed, message = Connections.edit_chock(data, i)
            if (committed is True):
                debug('Chocks & Bearings Form EDITED successfully')
                return render_template('successfulEdit.html')
            else:
                error('Problem EDITING Chocks & Bearings Form' + message)
                return render_template('error.html', message = message) #error message

@app.route('/add-email', methods = ['GET','POST'])#template for saving data from a webpage
def add_email():
    if request.method == 'POST':
        data = Requests.email_request_data(request)
        committed, message = Connections.add_email(data, Employee)
        if committed is True:
            debug('Email succesfully ADDED')
        else:
            error('Problem ADDING email - ' + message)
            return render_template('error.html', message = message) #error message

@app.route('/remove-email', methods = ['POST'])
def remove_email():
    if request.method == 'POST':
        data = Requests.email_request_data(request)
        committed, message = Connections.remove_email(data, Employee)
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
        roll = db.session.query(Roll).filter_by(roll_num=roll_num).first() #since we know this is only going to grab 1 result, we just grab the first item in the initial resulting list. Result is a roll object 
        grinds = db.session.query(Grind).filter_by(roll_num=roll_num).order_by(Grind.entry_time) #returns list of all grinds 
        info = db.session.query(Info).filter_by(mill=roll.mill, roll_type=roll.roll_type).first() #Returns the first item in the list
        graph = roll.generate_graphs(grinds, info)
        roll.generate_graphs_2(grinds, info, timedelta(weeks=52), False)
        roll.generate_graphs_2(grinds, info, timedelta(weeks=26), False)
        roll.generate_graphs_2(grinds, info, timedelta(weeks=13), False)
        stats1 = roll.avg_grind_stats(timedelta(weeks=52))
        stats2 = roll.avg_grind_stats(timedelta(weeks=26))
        stats3 = roll.avg_grind_stats(timedelta(weeks=13))
        return render_template('rollView.html', graph=graph, roll_num = roll_num, last_grinds=grinds, num_grinds=grinds.count(), roll = roll, info=info, stats1=stats1, stats2=stats2, stats3=stats3)



def reset_stats():
    db.session.query(Grind).delete()
    rolls = db.session.query(Roll).all()
    for roll in rolls:
        inches_above_scrap = random.randrange(1, 3)
        roll.diameter = roll.scrap_diameter + inches_above_scrap
        roll.approx_scrap_date = '12-12-12'
        roll.grinds_left = None
        roll.avg_grind = None
        roll.days_between_grinds = None
        roll.num_grinds = 0
        roll.scrapped = False
    db.session.commit()
    return
        
def advance_one_year(today):
    rolls = db.session.query(Roll).all()
    for roll in rolls:
        info = db.session.query(Info).filter_by(mill=roll.mill, roll_type=roll.roll_type)[0]
        day = today
        while (day <= today + datetime.timedelta(weeks=52) and roll.scrapped == False):
            diameter_lost = random.randrange(3, 6) * .01
            newGrind = Grind(roll_num=roll.roll_num, entry_time = day, HS_before = roll.diameter, MD_before = roll.diameter, TS_before = roll.diameter, HS_after = roll.diameter - diameter_lost, MD_after = roll.diameter - diameter_lost, TS_after = roll.diameter - diameter_lost, min_diameter_change = diameter_lost, max_deviation=0, min_deviation = 0, roll_length = 0, crowning_length = 0, crowning_angle = 0, crowning_bevel=0, min_diameter=roll.diameter - diameter_lost)
            roll.add_grind(newGrind)
            day = day + datetime.timedelta(days=info.days_between_grinds)
    db.session.commit()
    # for roll in rolls:
    #     print(roll.days_between_grinds)



if __name__ == "__main__":
    app.run()
    