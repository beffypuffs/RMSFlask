# anything connecting to SQL or access will be here for now

import datetime
import pyodbc as pp


def access_connect():
    try:
        conn = pp.connect('Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=E:\\RMS\\Access\\RSMS_IF.NET.mdb;')
    except pp.Error as e:
        print('error connecting to Access server: ' + str(e))
        exit()
    try:
        S_conn = pp.connect('Driver= {SQL Server};Server=localhost\\SQLEXPRESS;Database=rms;'
        'uid=rmsapp;pwd=ss1RMSpw@wb02')
    except pp.error as e:
        print("error connecting to SQL server" + str(e))
        exit()
    cur = conn.cursor()
    cur.execute('select * from Grind_Data')
    for row in cur.fetchall():
        insert = sql_insert('grind_raw', row) #generate insert message
        cur = S_conn.cursor()
        # print(insert)
        cur.execute(insert)
    delete_dups(S_conn)
    remove_fake_data(S_conn)
    S_conn.commit()


#Some of the data gets changed from access into python, this cleans it up for SQL. Only tested on Grind_Raw
def sql_insert(table, values):
    exec_message = 'INSERT INTO ' + table + ' VALUES ('
    first = True
    for item in values:
        if(first):
            if item is None or str(item) == '':
                exec_message += ' NULL'
            elif type(item) is str:
                exec_message += '\'' + item + '\''
            else:
                exec_message += str(item) 
            first = False
        else:
            if item is None or str(item) == '':
                exec_message += ', NULL'
            elif type(item) is str or datetime.datetime:
                exec_message += ',\'' + str(item) + '\''
            else:
                exec_message += ', ' + str(item) 
    exec_message += ')'
    return exec_message


def delete_dups(connection):#deletes duplicates using CTE. Can be simplified if we get admin priveleges
    cur = connection.cursor()
    cur.execute('WITH CTE([Entry_Time], dups) AS (SELECT [Entry_Time], ROW_NUMBER() OVER (PARTITION BY [Entry_Time] ORDER BY Id) AS dups FROM Grind_Raw) DELETE FROM CTE WHERE dups > 1')


def remove_fake_data(connection):#SQL data has some fake entries, won't need this function once we are getting live data
    cur = connection.cursor()
    cur.execute('DELETE FROM Grind_Raw WHERE Entry_Time > \'2020-09-16 8:00:00\'')


def remove_email(request):
    committed = False
    message = ""
    try: #Use this code whenever you connect to SQL server
        connection = pp.connect('Driver= {SQL Server};Server=localhost\\SQLEXPRESS;Database=rms;'
            'uid=rmsapp;pwd=ss1RMSpw@wb02') 
    except pp.Error as e: 
        message = ('error connecting to SQL server: ' + str(e))
        return committed, message

    badge_number = request.form['badge_number']
    name = request.form['nm']
    email = request.form['email']

    cur = connection.cursor()
    try:
        cur.execute(f'DELETE FROM employee WHERE badge_number = {badge_number} AND name = \'{name}\' AND email = \'{email}\';')
    except pp.Error as e:
        message = str(e) #returns error code if query fails
        return committed, message
    connection.commit()
    committed = True
    return committed, message


def add_email(request):
    committed = False
    message = ""
    try: #Use this code whenever you connect to SQL server
        connection = pp.connect('Driver= {SQL Server};Server=localhost\\SQLEXPRESS;Database=rms;'
            'uid=rmsapp;pwd=ss1RMSpw@wb02') 
    except pp.Error as e:
        message = ("error connecting to SQL Server: " + str(e)) #returns error type
        return committed, message

    badge_number = request.form['badge_number']
    name = request.form['nm']
    email = request.form['email']

    cur = connection.cursor()
    try:
        cur.execute('INSERT INTO employee VALUES(' + badge_number + ', \'' + name + '\', \'' + email + '\')')
    except pp.Error as e:
        message = str(e) #returns error code if query fails
        return committed, message
    connection.commit()
    committed = True
    return committed, message
        

def query_results(query, cols): #Displays roll information
    executed = False
    message = ""
    try: #Use this code whenever you connect to SQL server
        connection = pp.connect('Driver= {SQL Server};Server=localhost\\SQLEXPRESS;Database=rms;'
            'uid=rmsapp;pwd=ss1RMSpw@wb02') 
    except pp.Error as e:
        message = "error connecting to SQL Server: " + str(e) #returns error type
        return None, executed, message
    cur = connection.cursor() # Used to execute actions, might be able do more idk
    try:
        cur.execute(query) # Query
    except pp.Error as e:
        message = "error executing query: " + str(e)
        return None, executed, message
    data = cur.fetchall()    
    table_data = [] # The table of data we want to display
    # Add data into table data
    for row in data:
        data_row = []
        for col in range(cols):
            data_row.append(str(row[col]))
        # Array to hold a single data entry / Table row
        table_data.append(data_row)
    executed = True
    return table_data, executed, message

def add_chock(request):
    committed = False
    message = ""
    try: #Use this code whenever you connect to SQL server
        connection = pp.connect('Driver= {SQL Server};Server=localhost\\SQLEXPRESS;Database=rms;'
    'uid=rmsapp;pwd=ss1RMSpw@wb02') 
    except pp.Error as e:
        message = "error connecting to SQL Server: " + str(e) #returns error type
        return committed, message

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
    committed = True
    return committed, message
    