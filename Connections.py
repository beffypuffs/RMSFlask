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
    try: #Use this code whenever you connect to SQL server
        connection = pp.connect('Driver= {SQL Server};Server=localhost\\SQLEXPRESS;Database=rms;'
    'uid=rmsapp;pwd=ss1RMSpw@wb02') 
    except pp.Error as e: 
        print('error connecting to SQL server: ' + str(e))
        return committed

    badge_number = request.form['badge_number']
    name = request.form['nm']
    email = request.form['email']

    cur = connection.cursor()
    try:
        cur.execute(f'DELETE FROM employee WHERE badge_number = {badge_number} AND name = \'{name}\' AND email = \'{email}\';')
    except pp.Error as e:
        print('error deleting email: ' + str(e)) #returns error code if query fails
    connection.commit()
    committed = True
    return committed


def add_email(request):
    committed = False
    try: #Use this code whenever you connect to SQL server
        connection = pp.connect('Driver= {SQL Server};Server=localhost\\SQLEXPRESS;Database=rms;'
    'uid=rmsapp;pwd=ss1RMSpw@wb02') 
    except pp.Error as e:
        print("error connecting to SQL Server: " + str(e)) #returns error type
        return committed

    badge_number = request.form['badge_number']
    name = request.form['nm']
    email = request.form['email']

    cur = connection.cursor()
    try:
        cur.execute('INSERT INTO employee VALUES(' + badge_number + ', \'' + name + '\', \'' + email + '\')')
    except pp.Error as e:
        print('error inserting into SQL server' + str(e)) #returns error code if query fails
        return committed
    connection.commit()
    committed = True
    return committed
        

def table_data(): #Displays roll information
    try: #Use this code whenever you connect to SQL server
        connection = pp.connect('Driver= {SQL Server};Server=localhost\\SQLEXPRESS;Database=rms;'
        'uid=rmsapp;pwd=ss1RMSpw@wb02') 
    except pp.Error as e:
        message = "error connecting to SQL Server: " + str(e) #returns error type
        return message
    cur = connection.cursor() #used to execute actions, might be able do more idk
    cur.execute("Select *  From roll ORDER BY roll_num DESC")#query
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