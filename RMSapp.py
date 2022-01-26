from flask import Flask, redirect, url_for, render_template, request, g
from flask_mail import Mail, Message
import Connections
import Requests
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
    send_notification_email() # RELOCATE THIS TO SEND EMAIL WHEN REPLACEMENT SHOULD BE ORDERED
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

# function to send a notification email to registered users in the RMS
def send_notification_email():
    # create a connection w/ the database
    connection, conn_message = Connections.sql_connect()

    if conn_message == "connected":
        # get rolls to order IMMEDIATELY (1 year in advance)
        order_now_query = 'SELECT * FROM roll_new WHERE approx_scrap_date > DATEADD(year, -1, GETDATE());' 
        order_now, order_now_committed, message = Connections.query_results(connection, order_now_query)
        if not order_now_committed:
            return message

        # get rolls to order SOON (15 months in advance)
        order_soon_query = 'SELECT * FROM roll_new WHERE (approx_scrap_date > DATEADD(month, -15, GETDATE())) AND (approx_scrap_date < DATEADD(year, -1, GETDATE()))'
        order_soon, order_soon_committed, message = Connections.query_results(connection, order_soon_query)
        if not order_soon_committed:
            return message

        # get notification recipients from the RMS database
        recipients_query = 'SELECT email FROM employee;'
        recipients, recipients_committed, message = Connections.query_results(connection, recipients_query)
        if not recipients_committed:
            return message

        # send the notification email
        notif.send_noti_email(order_now, order_soon, RMS_EMAIL, 
            recipients, rms_mail)
    else:
        return conn_message

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