# anything connecting to SQL or access will be here for now

import datetime
from dateutil import relativedelta
import numpy as np
import math
import pyodbc as pp
"""
MAKE SURE THE PYODBC LINE IS COMMENTED IN, PYMSSQL IS COMMENTED OUT, AND YOU ARE USING THE RIGHT SQL_CONNECT d
"""
#import pymssql as pp
# import psycopg2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#Some of the data gets changed from access into python, this cleans it up for SQL.
def sql_insert(table, values):
    """Might have some utility eventually to build a sql insert, not sure if its worth the trouble """
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


# def delete_dups(connection):#deletes duplicates using CTE. Can be simplified if we get admin priveleges.
#     cur = connection.cursor()
#     cur.execute('WITH CTE([Entry_Time], dups) AS (SELECT [Entry_Time], ROW_NUMBER() OVER (PARTITION BY [Entry_Time] ORDER BY Id) AS dups FROM Grind_Raw) DELETE FROM CTE WHERE dups > 1')


# def remove_fake_data(connection):#SQL data has some fake entries, won't need this function once we are getting live data
#     cur = connection.cursor()
#     cur.execute('DELETE FROM Grind_Raw WHERE Entry_Time > \'2020-09-16 8:00:00\'')


def remove_email(connection, data):
    committed = False
    message = ""
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
    """Returns results of a SELECT query in table form
    Not every query uses this function, might be worth fixing
    """
    executed = False
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
    message = "database queried successfully"
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

# def sql_connect(): #Use on your own machine, other one is for kaiser
#     message = "connected"
#     try: #Use this code whenever you connect to SQL server
#         connection = pp.connect('Driver={SQL Server};Server=rmssql.database.windows.net;Database=RMSSQL;'
#     'uid=RMS;pwd=trpJ63iGY4F7mRj') 
#     except pp.Error as e:
#         message = "error connecting to SQL Server: " + str(e) #returns error type
#         print(message)
#         return None, message
#     return connection, message

def sql_connect(): #For JC's computer
    message = "connected"
    try: #Use this code whenever you connect to SQL server
        connection = pp.connect(server='rmssql.database.windows.net', user='RMS', password='trpJ63iGY4F7mRj', database='RMSSQL')
    except pp.Error as e:
        message = "error connecting to SQL Server: " + str(e) #returns error type
        print(message)
        return None, message
    return connection, message

def generate_graphs(roll, grinds, info): #not useful rn just messing around with matplotlib, we need a dataset for multiple rolls that we can use until we have enough data
    y = []
    x = []
    dates = []
    data_exists = False
    for grind in grinds:
        data_exists = True
        x.append(grind.entry_time)
        y.append(grind.HS_after)


    fig, ax = plt.subplots()
    other_diameter = calculate_12mo_diameter(info.scrap_diameter, info.days_between_rolls, info.avg_grind_diameter)

    if grinds.count() > 0:
        cur_day = datetime.datetime(x[-1].year, x[-1].month, x[-1].day)
        trend_x = []
        trend_y = []
        trend2_y = []
        trend2_x = []
        diameter_proj = roll.diameter
    
        while diameter_proj > info.scrap_diameter:#projection based on roll type average grind
            trend_y.append(diameter_proj)
            trend_x.append(cur_day)
            diameter_proj = diameter_proj - info.avg_grind_diameter
            cur_day = cur_day + datetime.timedelta(days=info.days_between_rolls) #CHANGE TO days_between_rolls WHEN U FINALIZE SQL DATABASE
        trend_y.append(info.scrap_diameter)
        trend_x.append(cur_day)

        diameter_proj = roll.diameter
        cur_day = datetime.datetime(x[-1].year, x[-1].month, x[-1].day)
        while diameter_proj > info.scrap_diameter: #projection based on specific rolls average grind
            print("in here")
            trend2_y.append(diameter_proj)
            trend2_x.append(cur_day)
            diameter_proj = diameter_proj - roll.avg_grind
            cur_day = cur_day + datetime.timedelta(days=roll.days_between_grinds)
        trend2_y.append(info.scrap_diameter)
        trend2_x.append(cur_day)
        plt.plot_date(trend_x,trend_y,'b-')
        plt.plot_date(trend2_x, trend2_y, 'g-')#
    
    ax.plot_date(x, y, markerfacecolor = 'CornflowerBlue', markeredgecolor = 'Red', zorder=10)
    plt.axhline(y=other_diameter, color='y', linestyle='-')
    plt.axhline(y=info.scrap_diameter, color='r', linestyle='-')
    
    fig.autofmt_xdate()
    ax.title.set_text(f'Diameter Over Time: Roll {roll.roll_num}')
    
    plt.xlabel('Date')
    plt.ylabel('Diameter (in.)')
    plt.savefig('static/images/Sample Graph.png')
    return plt


def calculate_12mo_diameter(scrap_diameter, days_between, avg_grind):
    if days_between > 180 and days_between < 250:
        return scrap_diameter + (avg_grind * 2)
    else:
        thing = math.ceil(365 / days_between)
        return scrap_diameter + (avg_grind * thing)

def update_scrap_date(db, Roll, Grinds, Info): #Updates the scrap date, checks if a roll needs to be scrapped
    rolls = db.session.query(Roll).all()
    for roll in rolls:
        info = db.session.query(Info).filter_by(mill=roll.mill, roll_type=roll.roll_type).first()# roll info
        grinds = db.session.query(Grinds).filter_by(roll_num=roll.roll_num).order_by(Grinds.entry_time.desc())
        if grinds.count() > 0:
            cur_day = grinds.first().entry_time
            diameter = roll.diameter
            grinds = 0
            while diameter > info.scrap_diameter:
                cur_day = cur_day + datetime.timedelta(days=info.days_between_rolls)
                diameter = diameter - info.avg_grind_diameter
                grinds = grinds + 1
            roll.approx_scrap_date = cur_day
            roll.grinds_left = grinds
            if grinds == 0:
                roll.scrapped = True
            else:
                roll.scrapped = False
    db.session.commit()

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





# generate_graphs(16043)