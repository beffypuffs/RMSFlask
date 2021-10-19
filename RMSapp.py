from flask import Flask, redirect, url_for, render_template, request
import pypyodbc as pp




app = Flask(__name__)


@app.route("/help")
def help_page():
    return render_template('help.html')


@app.route("/chocksMenu")
def chocksMenu():
    return render_template('chocksMenu.html')\
    

@app.route("/chocks")
def chocks():
    return render_template('chocks.html')


@app.route("/notifications")
def notification():
    return render_template('notifications.html')


@app.route("/")
def home():
    return query_results()


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
    # below is literally the entire first half of the html, move to text file and read from that
    page = """
    <!DOCTYPE html> 
<html lang = "en">
<head>
	<link href = "style.css" rel="stylesheet" type="text/css" >

	<title>RMS Home</title>

</head>
<body>
	<header>
	<!-- Help icon and links -->
	<div id="helpOption">
		<a href="http://127.0.0.1:5000/help">Help</a>
		<a href="http://127.0.0.1:5000//help"><img src="static/images/helpBtn.png" height="60" width="60" class = "helpBtn" alt="Help Button" /></a>
	</div>
	<!-- Main Kaiser logo and page navigation links -->
		<img src="static/images/logo.png" alt="Kaiser Aluminium Logo"/>
		<p style="text-align: center">
		<strong>Home Roll Management Page</strong>  |  <a href="http://127.0.0.1:5000/chocksMenu">Chocks and Bearings </a>  |  <a href="http://127.0.0.1:5000/notifications">Notification Settings</a>
		</p>
	</header>

	<main>
		<br>
		<br>
	<!-- big table with links to roll data and lots of data
		will need to activate filtering feature
		maybe a search bar sort of thing?-->
	<div>
	<table class = "center">
	<caption><strong>General Roll Information</strong>
	<!-- seach bar to look for any value in the roll table -->
	<input type = "text" id = "filter_input" onkeyup ="searchFunction()" placeholder = "Search" title="Type in desired table value ">
		<tr>
			<th><strong>Roll ID</strong></th>
			<th><strong>Status</strong></th> <!-- Will automatically determine red or green for not in use or in use-->
			<th><strong>Current Diameter</strong></th>
			<th><strong>Starting Diameter</strong></th>
			<th><strong>Mill</strong></th>
			<th><strong>Roll Type</strong></th>
			<th><strong>Manufacured Date</strong></th>
		</tr>"""
    for row in data:
        page += "<tr>"
        page += "<td> " + str(row[0]) + "</td>"
        page += "<td> " + str(row[1]) + "</td>"
        page += "<td> " + str(row[2]) + "</td>" #always null, ask about it on monday
        page += "<td> " + str(row[3]) + "</td>"
        page += "<td> " + str(row[4]) + "</td>"
        page += "<td> " + str(row[5]) + "</td>"
        page += "<td> " + str(row[6]) + "</td>"
        page += "</tr>"
        
    #below this is literally the entire second half of index.html
    page += """
    </table> 
	</div>
	</main>
<script>
	//Filtering function for the search function to look through entire table for the value
	function searchFunction() {
    let tabel, filter, input, tr, td, i;
    input = document.getElementById("filter_input");
    filter = input.value.toUpperCase();
    tabel = document.getElementById("roll_table");
    tr = document.getElementsByTagName("tr");
    for (i = 1; i < tr.length; i++) {
        if (tr[i].textContent.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = "";
        } else {
            tr[i].style.display = "none";
			}
		}
	}

</script>
</body>
</html> 
"""
    return page




        


if __name__ == "__main__":
    app.run()