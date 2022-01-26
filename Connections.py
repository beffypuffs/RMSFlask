# anything connecting to SQL or access will be here for now

import datetime
import numpy as np
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


# def remove_fake_data(connection):#SQL data has some fake entries, won't need this function once we are getting live data
#     cur = connection.cursor()
#     cur.execute('DELETE FROM Grind_Raw WHERE Entry_Time > \'2020-09-16 8:00:00\'')


def remove_email(connection, data):
    committed = False
    message = ""
    try: #Use this code whenever you connect to SQL server
        connection = pp.connect('Driver= {SQL Server};Server=localhost\\SQLEXPRESS;Database=rms;'
            'uid=rmsapp;pwd=ss1RMSpw@wb02') 
    except pp.Error as e: 
        message = ('error connecting to SQL server: ' + str(e))
        return committed, message

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
    #print('INSERT INTO employee VALUES(' + badge_number + ', \'' + name + '\', \'' + email + '\')')
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

def sql_connect(): #not used, eventually will return current sql connection or start a new one if it hasn't been called
    # connection = psycopg2.connect(dbname='RMS',user='rmsAdmin',password='1029384756', host '')  #change to your ip
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
    #connection, message = sql_connect()
    #cur = connection.cursor()
    # roll_num = 1619
    # cur.execute(f'SELECT Roll_diameter_HS_After, Entry_Time FROM Grind_Raw WHERE Roll_Number={roll_num} ORDER BY Entry_Time')
    # data = cur.fetchall()
    y1 = [130.60,130.54, 130.48, 130.4, 130.32, 129.4, 129.32, 129.24, 129.16, 129.08, 129, 128.9, 128.8, 128.7, 128.6, 128.5, 128.4, 128.3, 128.2, 128.1, 128, 127.9, 127.8, 127.7, 127.6, 127.5]
    x = [datetime.datetime(2021, 3, 10, 12, 12, 12), datetime.datetime(2021, 4, 12, 12, 12, 12), datetime.datetime(2021, 5, 14, 12, 12, 12),
        datetime.datetime(2021, 6, 17, 12, 12, 12), datetime.datetime(2021, 7, 20, 12, 12, 12), datetime.datetime(2021,8, 23, 12, 12, 12),
        datetime.datetime(2021, 9, 24, 12, 12, 12), datetime.datetime(2021, 10, 28, 12, 12, 12), datetime.datetime(2021, 12, 1, 12, 12, 12),
        datetime.datetime(2022, 1, 1, 12, 12, 12), datetime.datetime(2022, 2, 1, 12, 12, 12), datetime.datetime(2022, 3, 1, 12, 12, 12), datetime.datetime(2022, 4, 1, 12, 12, 12),
        datetime.datetime(2022, 5, 1, 12, 12, 12), datetime.datetime(2022, 6, 1, 12, 12, 12), datetime.datetime(2022, 7, 1, 12, 12, 12), datetime.datetime(2022, 8, 1, 12, 12, 12), 
        datetime.datetime(2022, 9, 1, 12, 12, 12), datetime.datetime(2022, 10, 1, 12, 12, 12), datetime.datetime(2022, 11, 1, 12, 12, 12), datetime.datetime(2022, 12, 1, 12, 12, 12),
        datetime.datetime(2023, 1, 1, 12, 12, 12), datetime.datetime(2023, 2, 1, 12, 12, 12), datetime.datetime(2023, 3, 1, 12, 12, 12), datetime.datetime(2023, 4, 1, 12, 12, 12),
        datetime.datetime(2023, 5, 1, 12, 12, 12)]
    # for row in data:
    #     x.append(row[1])
    #     y.append(row[0])
    fig, ax = plt.subplots()
    ax.plot_date(x, y1, markerfacecolor = 'CornflowerBlue', markeredgecolor = 'Red', zorder=10)
    plt.axhline(y=120, color='y', linestyle='-')
    plt.axhline(y=117, color='r', linestyle='-')
    fig.autofmt_xdate()
    ax.set_xlim([datetime.date(2020, 12, 25), datetime.date(2030, 2, 1)])
    ax.set_ylim(100, 140)
    x2 = np.array([datetime.date(2020, 12, 25), datetime.date(2030, 2, 1)])
    y2 = np.array([130.60, 118])
    plt.plot(x2, y2, color='g', zorder=0)
    ax.title.set_text(f'Diameter Over Time: Roll {roll_num}')
    plt.legend(['Grinds', 'Needs Replacement', 'Scrapped', 'Projection'])
    plt.xlabel('Date')
    plt.ylabel('Diameter (in.)')
    plt.savefig('static\\images\\Sample Graph.png')
    
    
    # fig.title('Diameter Over Time')
    
    # plt.scatter(x,y)

    # # plt.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=(1, 15)))
    # plt.xlabel('Grind Date/Time')
    # plt.ylabel('Diameter')
    # plt.title('Diameter over time')
    # plt.savefig('static\\images\\Sample Graph.png')
    
    # return plt

# generate_graphs()



    
    