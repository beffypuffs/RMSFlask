from flask import Flask, redirect, url_for, render_template, request
import pypyodbc as pp




app = Flask(__name__)


@app.route("/")
def help_page():
    return render_template('help.html')


@app.route("/chocks")
def chocks():
    return render_template('chocks.html')


@app.route("/notifications")
def notification():
    return render_template('notifications.html')


@app.route("/home")
def home():
    return render_template('index.html')


#Replace with /index when its finished
@app.route("/queryresults")
def query():
    #return query_results()
    return render_template('rollData.html')


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
        except pp.Error as e:
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




def query_results(): #Displays roll information
    try: #Use this code whenever you connect to SQL server
        connection = pp.connect('Driver= {SQL Server};Server=localhost\\SQLEXPRESS;Database=rms;'
        'uid=rmsapp;pwd=ss1RMSpw@wb02') 
    except pp.Error as e:
        message = "error connecting to SQL Server: " + str(e) #returns error type
        return message
    cur = connection.cursor() #used to execute actions, might be able do more idk
    cur.execute("Select *  From roll ORDER BY roll_num DESC")#query
    data = cur.fetchall()
    page = "<!DOCTYPE html><html lang = \"en\"><body>"#May be a better way to have html files interact with flask, right now it just writes the html each time this runs
    for row in data:
        page += "=============<br>"
        page += "roll_num: " + str(row[0]) + "<br>"
        page += "roll_mate: " + str(row[1])+ "<br>" #always null, ask about it on monday
        page += "current_diameter: " + str(row[2]) + "<br>"
        page += "starting_diameter: " + str(row[3]) + "<br>"
        page += "mill: " + str(row[4]) + "<br>"
        page += "roll_type: " + str(row[5]) + "<br>"
        page += "status: " + str(row[6]) + "<br>" #also null
        page += "manufactured_date: " + str(row[7]) + "<br>"#ditto
    page += "</body></html>"

    file = open("rollData.html", "w")
    file.write(page)
    file.close()
    return page




        


if __name__ == "__main__":
    app.run()