# anything connecting to SQL or access will be here for now

import datetime
from dateutil import relativedelta
import numpy as np
import math
import pyodbc as pp
import psycopg2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def access_connect(): #irrelevant now
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
    #remove_fake_data(S_conn)
    S_conn.commit()


#Some of the data gets changed from access into python, this cleans it up for SQL.
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


def delete_dups(connection):#deletes duplicates using CTE. Can be simplified if we get admin priveleges.
    cur = connection.cursor()
    cur.execute('WITH CTE([Entry_Time], dups) AS (SELECT [Entry_Time], ROW_NUMBER() OVER (PARTITION BY [Entry_Time] ORDER BY Id) AS dups FROM Grind_Raw) DELETE FROM CTE WHERE dups > 1')


# def remove_fake_data(connection):#SQL data has some fake entries, won't need this function once we are getting live data
#     cur = connection.cursor()
#     cur.execute('DELETE FROM Grind_Raw WHERE Entry_Time > \'2020-09-16 8:00:00\'')


def remove_email(connection, data):
    committed = False
    message = ""
    # try: #Use this code whenever you connect to SQL server
    #     connection, message = sql_connect()
    # except pp.Error as e: 
    #     message = ('error connecting to SQL server: ' + str(e))
    #     return committed, message

    badge_number = data[0]
    name = data[1]
    email = data[2]

    cur = connection.cursor()
    try:
        cur.execute(f'DELETE FROM employee WHERE badge_number = {badge_number} AND name = \'{name}\' AND email = \'{email}\';')
    except pp.Error as e:
        message = str(e) #returns error code if query fails
        return committed, message
    connection.commit()
    committed = True
    return committed, message


def add_email(connection, data):
    committed = False
    message = ""
    badge_number = data[0]
    name = data[1]
    email = data[2]
    cur = connection.cursor()
    try:
        cur.execute('INSERT INTO employee VALUES(' + badge_number + ', \'' + name + '\', \'' + email + '\')')
    except pp.Error as e:
        message = str(e) #returns error code if query fails
        return committed, message
    connection.commit()
    committed = True
    return committed, message
        

def query_results(connection, query, cols): #Displays roll information
    executed = False
    message = ""
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

def add_chock(connection, data):
    committed = False
    message = ""
    cur = connection.cursor()
    #INPUT SANITATION
    try:
        message = sql_insert('report', data)
        cur.execute(message)
       #  cur.execute(f'INSERT INTO report VALUES({date}, {chock_nu')
    except pp.Error as e:
        return committed, str(e) #returns error code if query fails
    connection.commit()
    committed = True
    return committed, message

def remove_chock(connection, data):
    committed = False
    message = ""
    cur = connection.cursor()
    date = data[0]
    badge_num = data[52]

    # comments = request.form['comments']
    cur.execute(f'DELETE FROM report WHERE date = \'{date}\' AND badge_number = \'{badge_num}\'')
    connection.commit()
    return True, "Successfully removed"

def edit_chock(connection, data): #only works when date and bage_number are not changed, needs work in the future
    committed, message = remove_chock(connection, data)
    if (committed is True):
        committed, message = add_chock(connection, data)
    else:
        print (committed)
        print(message)
    return committed, message

# def sql_connect(): #not used, eventually will return current sql connection or start a new one if it hasn't been called
#     message = "connected"
#     try: #Use this code whenever you connect to SQL server
#         connection = pp.connect('Driver= {SQL Server};Server=localhost\\SQLEXPRESS;Database=rms;')
#     except pp.Error as e:
#         message = "error connecting to SQL Server: " + str(e) #returns error type
#         print(message)
#         return None, message
#     return connection, message

def sql_connect(): #Use on your own machine, other one is for kaiser
    message = "connected"
    try: #Use this code whenever you connect to SQL server
        connection = pp.connect('Driver={SQL Server};Server=rmssql.database.windows.net;Database=RMSSQL;'
    'uid=RMS;pwd=trpJ63iGY4F7mRj') 
    except pp.Error as e:
        message = "error connecting to SQL Server: " + str(e) #returns error type
        print(message)
        return None, message
    return connection, message

def generate_graphs(roll_num): #not useful rn just messing around with matplotlib, we need a dataset for multiple rolls that we can use until we have enough data
    connection, message = sql_connect()
    cur = connection.cursor()
    # scrap_date = datetime.date()
    scrap_diameter = None
    mill = None
    roll_type = None
    y = []
    x = []
    dates = []

    cur.execute(f'SELECT * FROM roll_new WHERE roll_num={roll_num}')
    roll_data = cur.fetchall()
    for row in roll_data:
        scrap_diameter = row[2]
        mill = row[5]
        roll_type = row[6]
        diameter = row[1]

    cur.execute(f'SELECT * FROM roll_info WHERE mill = \'{mill}\' AND roll_type = \'{roll_type}\'')
    roll_info = cur.fetchall()
    print(mill)
    print(roll_type)


    for row in roll_info:
        avg_grind = row[3]
        days_between = row[4]

    cur.execute(f'SELECT * FROM grind_new WHERE roll_num={roll_num} ORDER BY min_diameter DESC')
    grind_data = cur.fetchall()
    data_exists = False
    for row in grind_data:
        data_exists = True
        date = datetime.datetime.strptime(row[2], '%Y-%m-%d')
        dates.append(date)
        x.append(date)
        y.append(row[1])


    fig, ax = plt.subplots()
    other_diameter = calculate_12mo_diameter(scrap_diameter, days_between, avg_grind)

    if data_exists is True:
        cur_day = datetime.datetime(x[-1].year, x[-1].month, x[-1].day)
        trend_x = []
        trend_y = []
        diameter_proj = diameter
    
        while diameter_proj > scrap_diameter:
            trend_y.append(diameter_proj)
            trend_x.append(cur_day)
            diameter_proj = diameter_proj - avg_grind
            cur_day = cur_day + datetime.timedelta(days=days_between)
        trend_y.append(scrap_diameter)
        trend_x.append(cur_day)
            

        plt.plot_date(trend_x,trend_y,'b-')
    

    

    
    ax.plot_date(x, y, markerfacecolor = 'CornflowerBlue', markeredgecolor = 'Red', zorder=10)
    plt.axhline(y=other_diameter, color='y', linestyle='-')
    plt.axhline(y=scrap_diameter, color='r', linestyle='-')
    
        
        

    #ax.xaxis.set_major_formatter(
    # mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
    #ax.set_xlim([datetime.date(2020, 12, 25), datetime.date(2030, 2, 1)])
    # ax.set_xlim([datetime.date(2020, 1, 26), datetime.date(2025, 2, 1)])
    fig.autofmt_xdate()
    ax.title.set_text(f'Diameter Over Time: Roll {roll_num}')
    
    plt.xlabel('Date')
    plt.ylabel('Diameter (in.)')
    plt.savefig('static\\images\\Sample Graph.png')

def update_roll_info(roll_num):
    connection, message = sql_connect()
    cur = connection.cursor()
    cur.execute()

def calculate_12mo_diameter(scrap_diameter, days_between, avg_grind):
    if days_between > 180 and days_between < 250:
        return scrap_diameter + (avg_grind * 2)
    else:
        thing = math.ceil(365 / days_between)
        return scrap_diameter + (avg_grind * thing)

def trendline(roll_num, mill, type):
    pass

def populate_data(): # dont run this on kaiser's server, its just to make fake data
    connection, message = sql_connect()
    cur = connection.cursor()
    cur.execute(f'SELECT * FROM roll_new')
    roll_data = cur.fetchall()
    for row in roll_data:
            roll_num = row[0]
            diameter = row[1]
            scrap_diameter = row[2]
            mill = row[5]
            roll_type = row[6]

            cur.execute(f'SELECT * FROM roll_info WHERE mill = \'{mill}\' AND roll_type = \'{roll_type}\'')
            roll_info = cur.fetchall()
            avg_grind = roll_info[0][3]
            days_between = roll_info[0][4]
            cur_day = datetime.date.today()

            while cur_day > datetime.date(2019, 1, 21):
            #   cur.execute(f'INSERT INTO grind_new VALUES(roll_num = {roll_num}, min_diameter = {diameter}, grind_date = TO_DATE(\'{cur_day.year}-{cur_day.month}-{cur_day.year}\', \'YYYY-MM-DD\'), min_diameter_change = {avg_grind})')
                print(f'types: {type(roll_num)}, {type(diameter)},  {type(cur_day)},  {type(avg_grind)}')
                message = f'INSERT INTO grind_new VALUES({roll_num}, {diameter}, \'{cur_day}\', {avg_grind})'
                print(message)
                cur.execute(message)
                cur_day = cur_day - datetime.timedelta(days=days_between)
                diameter = diameter + avg_grind
    connection.commit()

def update_scrap_date():
    connection, message = sql_connect()
    cur = connection.cursor()
    cur.execute(f'SELECT * FROM roll_new')
    roll_data = cur.fetchall()
    for row in roll_data:
        roll_num = row[0]
        diameter = row[1]
        scrap_diameter = row[2]
        mill = row[5]
        roll_type = row[6]
        print(mill)
        print(roll_type)
        cur.execute(f'SELECT * FROM roll_info WHERE mill = \'{mill}\' AND roll_type = \'{roll_type}\'')
        roll_info = cur.fetchall()
        print(roll_info)
        avg_grind = roll_info[0][3]
        days_between = roll_info[0][4]

        cur.execute(f'SELECT * FROM grind_new WHERE roll_num = {roll_num} ORDER BY grind_date ASC')
        grind_data = cur.fetchall()
        if len(grind_data) != 0:
            cur_day = datetime.datetime.strptime(grind_data[-1][2], '%Y-%m-%d').date()
        
            while diameter > scrap_diameter:
                cur_day = cur_day + datetime.timedelta(days=days_between)
                diameter = diameter - avg_grind

            message = f'UPDATE roll_new SET approx_scrap_date = \'{cur_day}\' WHERE roll_num = {roll_num}'
            print(cur_day)
            print(message)
            cur.execute(message)
# populate_data()
    connection.commit()

def update_diameter():
    connection, message = sql_connect()
    cur = connection.cursor()
    cur.execute(f'SELECT * FROM roll_new')
    roll_data = cur.fetchall()
    for row in roll_data:
        roll_num = row[0]
        print(roll_num)
        cur.execute(f'SELECT * FROM grind_new WHERE roll_num = {roll_num} ORDER BY min_diameter ASC')
        grind_data = cur.fetchall()
        if len(grind_data) > 0:
            #print(grind_data[0][0])
            #print(grind_data[0][3])
            diameter = grind_data[0][1]

            #print(diameter)
            message = f'UPDATE roll_new SET diameter = {diameter} WHERE roll_num = {roll_num}'
            print(message)
            cur.execute(message)
    connection.commit()

#update_diameter()

#update_scrap_date()
    
def rolls_order_now(connection):
    """Gets a table of rolls whose replacements must be ordered immediately (They are within 
    a year of needing to be replaced). Query RMS database for rolls that are less than 12 
    months (1 year) from their approximate scrap date. Put this data in a list and return the
    list aling with a boolean value representing whether the query was executed successfully 
    and a connection results message
    """
    executed = False
    query = 'SELECT * FROM roll_new WHERE (approx_scrap_date < DATEADD(year, 1, GETDATE()) \
        AND approx_scrap_date > GETDATE()) ORDER BY approx_scrap_date;' 
    cur = connection.cursor()
    try:
        cur.execute(query)
        data = cur.fetchall()
        table_data = []
        for row in data:
            data_row = []
            for col in range(len(row)):
                data_row.append(str(row[col]))
            table_data.append(data_row)
        executed = True
        return table_data, executed, "Database Queried Successfully - Connections.rolls_order_now()"
    except pp.Error as e:
        message = "error executing query: " + str(e)
        return None, executed, message

def rolls_order_soon(connection):
    """Gets a table of rolls whose replacements must be ordered soon (They are 12 - 15 
    months of needing to be replaced). Query RMS database for rolls that are between 12 
    and 15 months from their approximate scrap date. Put this data in a list and return the
    list aling with a boolean value representing whether the query was executed successfully 
    and a connection results message.
    """
    executed = False
    message = ""
    query = 'SELECT * FROM roll_new WHERE (approx_scrap_date < DATEADD(month, 15, GETDATE())) \
        AND approx_scrap_date > GETDATE() AND (approx_scrap_date > DATEADD(YEAR, 1, GETDATE())) \
        ORDER BY approx_scrap_date;'
    cur = connection.cursor()
    try:
        cur.execute(query)
        data = cur.fetchall()
        table_data = []
        for row in data:
            data_row = []
            for col in range(len(row)):
                data_row.append(str(row[col]))
            table_data.append(data_row)
        executed = True
        return table_data, executed, "Database Queried Successfully - Connections.rolls_order_soon()"
    except pp.Error as e:
        message = "error executing query: " + str(e)
        return None, executed, message
    
def email_notification_recipients(connection):
    """Gets a list of the emails registered to receive notification emails from the RMS
    database. Query the database for the registered employee emails . Put this data in a 
    list and return the list aling with a boolean value representing whether the query 
    was executed successfully and a connection results message.
    """
    executed = False
    query = 'SELECT email FROM employee;'
    cur = connection.cursor()
    try:
        cur.execute(query)
        email_recipients = [employee[0] for employee in cur.fetchall()]
        executed = True
        return email_recipients, executed, "Database Queried Successfully - Connections.email_notification_recipients()"
    except pp.Error as e:
        message = "error executing query: " + str(e)
        return None, executed, message
