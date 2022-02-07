from flask import Flask, redirect, url_for, render_template, request, g
from flask_mail import Mail, Message
import Connections
import Requests


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