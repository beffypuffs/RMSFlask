from datetime import date
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
    data = query_results("Select *  FROM report ORDER BY date DESC", 7)
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
    data = query_results("Select *  FROM roll ORDER BY roll_num DESC", 7)
    return render_template("index.html", headings=headings, data=data)



#Replace with /index when its finished
@app.route("/queryresults") #this will eventually replace home/index.html
def query():
    #return query_results()
    return render_template('rollData.html')#temporary link

#Add chock function
@app.route('/add-chock', methods = ['GET','POST'])
def add_chock():
    if request.method == 'POST':
        try: #Use this code whenever you connect to SQL server
            connection = pp.connect('Driver= {SQL Server};Server=localhost\\SQLEXPRESS;Database=rms;'
        'uid=rmsapp;pwd=ss1RMSpw@wb02') 
        except pp.Error as e:
            message = "error connecting to SQL Server: " + str(e) #returns error type
            return message

        date = request.form['date'],
        chock_number = request.form['chock-num'],
        position = request.form['position'],
        reason = request.form['reasons_d_and_i'],
        visible_chock_numbers = request.form['obvi'],
        lifiting_bolt_thread_condition = request.form['lifting'],
        cover_end_condition = request.form['cover'],
        bell_o_ring_condition = request.form['end-bell'],
        thrust_collar = request.form['thrust'],
        lockkeepers = request.form['locks'],
        liner_plates = request.form['liner'],
        inboard_radial_seals_replaced = request.form['num-rep'],
        inboard_face_seal = request.form['seals1'],
        outboard_radial_seal = request.form['seals2'],
        load_zone_from_mill = request.form['mill1'],
        load_zone_to_mill = request.form['mill2'],
        bearing_grease_condition = request.form['bearing-grease'],
        bearing_mfg = request.form['mfg'],
        bearing_serial_number = request.form['sn'],
        is_sealed = request.form['sealed'],
        seals_replaced = request.form['seals-rep'],
        cup_a = request.form['cupA'],
        cup_bd = request.form['cupB'],
        cup_e = request.form['cupE'],
        race_a = request.form['raceA'],
        race_b = request.form['raceB'],
        race_d = request.form['raceD'],
        race_e = request.form['raceE'],
        bearing_status = request.form['bearing-condition'],
        different_bearing_installed = request.form['diff-bearing'],
        bearing_mfg_new = request.form['textMFG'],
        serial_number_new = request.form['MFGsn'],
        sealed_new = request.form['sealed2'],
        chock_bore_round = request.form['chockBoreRound'],
        chock_bore = request.form['chockBoreOOR'],
        no_rust = request.form['wearOrRust'],
        grease_purged = request.form['purgeGrease'],
        spots_dings = request.form['spots-dings'],
        manual_pack = request.form['manual-pack'],
        lube_bore = request.form['lube-bore'],
        grease_packed_bearings = request.form['dropped'],
        height_shoulder = request.form['droppedA'],
        bearing_depth = request.form['droppedB'],
        shims_needed = request.form['droppedDifference'],
        was_paper_used = request.form['paper-used'],
        by_hand = request.form['shim'],
        was_torqued = request.form['phases'],
        ancillary_installed = request.form['ancillary'],
        grease_pack_sealed = request.form['greasePack'],
        chock_ready_for_installation = request.form['ready'],
        comments  = request.form['comments'],
        mill = request.form['roll_mill'],
        badge_number = request.form['badge_number'],
        roll_type = request.form['roll_type']
        cur = connection.cursor()
        #INPUT SANITATION
        #print('INSERT INTO employee VALUES(' + badge_number + ', \'' + name + '\', \'' + email + '\')')
        try:
            # first draft of this! I need to ask jeff what some values should be and check which ones are numbers since I'm assuming most of these are being interpreted as strings
            cur.execute('INSERT INTO report VALUES(' + date + ', ' + chock_number + ', \'' + position + '\', \'' + reason + '\', \'' + visible_chock_numbers + '\', \'' + lifiting_bolt_thread_condition + 
            '\', \'' + cover_end_condition + '\', \'' + bell_o_ring_condition + '\', \'' + thrust_collar + '\', \'' + '\', \'' + lockkeepers + '\', \'' + liner_plates + '\', \'' + inboard_radial_seals_replaced +
            '\', \'' + inboard_face_seal + '\', \'' + outboard_radial_seal + '\', \'' + load_zone_from_mill + '\', \'' + load_zone_to_mill + '\', \'' + bearing_grease_condition + '\', \'' + bearing_mfg +
            '\', \'' + bearing_serial_number + '\', \'' + is_sealed + '\', \'' + seals_replaced + '\', \'' + cup_a + '\', \'' + cup_bd + '\', \'' + cup_e + '\', \'' + race_a + '\', \'' + race_b +
            '\', \'' + race_d + '\', \'' + race_e + '\', \'' + bearing_status + '\', \'' + different_bearing_installed + '\', \'' + bearing_mfg_new + '\', \'' + serial_number_new + '\', \'' + sealed_new +
            '\', \'' + chock_bore_round + '\', \'' + chock_bore + '\', \'' + no_rust + '\', \'' + grease_purged + '\', \'' + spots_dings + '\', \'' + manual_pack + '\', \'' + lube_bore + '\', \'' + grease_packed_bearings + 
            '\', \'' + height_shoulder + '\', \'' + bearing_depth + '\', \'' + shims_needed + '\', \'' + was_paper_used + '\', \'' + by_hand + '\', \'' + was_torqued + '\', \'' + ancillary_installed +
            '\', \'' + grease_pack_sealed + '\', \'' + chock_ready_for_installation + '\', \'' + comments + '\', \'' + mill + '\', \'' + badge_number + '\', \'' + roll_type + 
            '\')')
        except pp.Error as e:
            return str(e) #returns error code if query fails
        connection.commit()
    return 'thing'

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




def query_results(query, cols): #Displays roll information
    try: #Use this code whenever you connect to SQL server
        connection = pp.connect('Driver= {SQL Server};Server=localhost\\SQLEXPRESS;Database=rms;'
        'uid=rmsapp;pwd=ss1RMSpw@wb02') 
    except pp.Error as e:
        message = "error connecting to SQL Server: " + str(e) #returns error type
        return message
    cur = connection.cursor() # Used to execute actions, might be able do more idk
    cur.execute(query) # Query
    data = cur.fetchall()
    table_data = [] # The table of data we want to display
    # Add data into table data
    for row in data:
        data_row = []
        for col in range(cols):
            data_row.append(str(row[col]))
        # Array to hold a single data entry / Table row
        table_data.append(data_row)
    return table_data


        


if __name__ == "__main__":
    app.run()