from flask import Flask, redirect, url_for, render_template, request
import pyodbc as pp


app = Flask(__name__)


@app.route("/help")
def help_page():
    return render_template('help.html')


@app.route("/chocksMenu")
def chocksMenu():
    return render_template('chocksMenu.html')


@app.route("/chocksView")
def chocksView():
    headings = ("Roll ID", "Status", "Current Diameter", "Starting Diameter", "Mill", "Roll Type", "Manufacture Date")
    data = query_results("Select *  FROM report ORDER BY date DESC")
    return render_template('chocksView.html', headings=headings, data=data)
    

@app.route("/chocks")
def chocks():
    return render_template('chocks.html')


@app.route("/notifications")
def notification():
    return render_template('notifications.html')


@app.route("/")
def home():
    headings = ("Roll ID", "Status", "Current Diameter", "Starting Diameter", "Mill", "Roll Type", "Manufacture Date")
    data = query_results("Select *  From roll ORDER BY roll_num DESC")
    return render_template("index.html", headings=headings, data=data)


#Replace with /index when its finished
@app.route("/queryresults") #this will eventually replace home/index.html
def query():
    #return query_results()
    return render_template('rollData.html')#temporary link


@app.route('/add-email', methods = ['GET','POST'])#template for saving data from a webpage
def add_email():
    if request.method == 'POST':
        try: #Use this code whenever you connect to SQL server
            connection = pp.connect('Driver= {SQL Server};Server=localhost\\SQLEXPRESS;Database=rms;'
        'uid=rmsapp;pwd=ss1RMSpw@wb02') 
        except pp.Error as e:
            message = "error connecting to SQL Server: " + str(e) #returns error type
            return message

        badge_number = request.form['badge_number']
        name = request.form['nm']
        email = request.form['email']

        cur = connection.cursor()
        #INPUT SANITATION
        #print('INSERT INTO employee VALUES(' + badge_number + ', \'' + name + '\', \'' + email + '\')')
        try:
            cur.execute('INSERT INTO employee VALUES(' + badge_number + ', \'' + name + '\', \'' + email + '\')')
        except pp.Error as e:
            return str(e) #returns error code if query fails
        connection.commit()
    return 'thing'

@app.route('/remove-email', methods = ['POST'])
def remove_email():
     if request.method == 'POST':
        try: #Use this code whenever you connect to SQL server
            connection = pp.connect('Driver= {SQL Server};Server=localhost\\SQLEXPRESS;Database=rms;'
        'uid=rmsapp;pwd=ss1RMSpw@wb02') 
        except pp.Error as e: #eventually
            message = "error connecting to SQL Server: " + str(e) #returns error type
            return message

        badge_number = request.form['badge_number']
        name = request.form['nm']
        email = request.form['email']

        cur = connection.cursor()
        #INPUT SANITATION
        # print(f'DELETE FROM employee WHERE badge_number = {badge_number} AND name = {name} AND email = {email};')
        try:
            cur.execute(f'DELETE FROM employee WHERE badge_number = {badge_number} AND name = \'{name}\' AND email = \'{email}\';')
        except pp.Error as e:
            return str(e) #returns error code if query fails
        connection.commit()
        # cur.execute(f'INSERT INTO employee VALUES({badge_number}, \'{name}\', \'{email}\')')
        return 'thing'




def query_results(query): #Displays roll information
    try: #Use this code whenever you connect to SQL server
        connection = pp.connect('Driver= {SQL Server};Server=localhost\\SQLEXPRESS;Database=rms;'
        'uid=rmsapp;pwd=ss1RMSpw@wb02') 
    except pp.Error as e:
        message = "error connecting to SQL Server: " + str(e) #returns error type
        return message
    cur = connection.cursor() #used to execute actions, might be able do more idk
    cur.execute(query)#query
    data = cur.fetchall()
    table_data = [] # The table of data we want to display
    # Add data into table data
    for row in data:
        data_row = [] # Array to hold a single data entry / Table row
        data_row.append(str(row[0]))
        data_row.append(str(row[1]))
        data_row.append(str(row[2])) #always null, ask about it on monday
        data_row.append(str(row[3]))
        data_row.append(str(row[4]))
        data_row.append(str(row[5]))
        data_row.append(str(row[6]))
        table_data.append(data_row)
    return table_data


        


if __name__ == "__main__":
    app.run()