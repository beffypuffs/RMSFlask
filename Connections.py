# anything connecting to SQL or access will be here for now

import datetime
from dateutil import relativedelta
import numpy as np
import math
from models import db
#import pyodbc as pp
"""
MAKE SURE THE PYODBC LINE IS COMMENTED IN, PYMSSQL IS COMMENTED OUT, AND YOU ARE USING THE RIGHT SQL_CONNECT d
"""
import pymssql as pp
# import psycopg2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates



def remove_email(data, Employee):
    committed = False
    message = ""
    badge_number = data[0]
    name = data[1]
    email = data[2]
    try:
        db.session.query(Employee).filter_by(badge_number=badge_number, name=name, email=email).delete()
    except pp.Error as e:
        message = str(e) #returns error code if query fails
        return committed, message
    db.session.commit()
    committed = True
    return committed, message


def add_email(data, Employee):
    committed = False
    message = ""
    badge_number = data[0]
    name = data[1]
    email = data[2]
    try:
        newEmployee = Employee(name=name, badge_number=badge_number, email=email)
        db.session.add(newEmployee)
        # cur.execute('INSERT INTO employee VALUES(' + badge_number + ', \'' + name + '\', \'' + email + '\')')
    except pp.Error as e:
        message = str(e) #returns error code if query fails
        return committed, message
    db.session.commit()
    committed = True
    return committed, message
        

def add_chock(form_data, Report):
    try:
        #message = sql_insert('report', data)
        newReport = Report(data=form_data)
        db.session.add(newReport)
    except pp.Error as e:
        return committed, str(e) #returns error code if query fails
    db.session.commit()
    committed = True
    message = "Chock Succesfully Added"
    return committed, message

def remove_chock(data, Report):
    committed = False
    date = data[0]
    badge_num = data[52]
    # comments = request.form['comments']
    db.session.query(Report).filter_by(date=date, badge_number=badge_num)
    return True, "Successfully removed"

def edit_chock(data, Report, i): #only works when date and bage_number are not changed, needs work in the future
    # committed, message = remove_chock(data, Report)
    # if (committed is True):
    #     committed, message = add_chock(data, Report)
    # return committed, message
    reports = db.session.query(Report).filter_by(ID=i).all()
    
    if len(reports) > 1 or len(reports) == 0: #i dont think it will ever be 0 since you hit edit 
        print("Something went wrong")
    else:
        reports[0].edit(data)
        

def generate_graphs(roll, grinds, info): #not useful rn just messing around with matplotlib, we need a dataset for multiple rolls that we can use until we have enough data
    y = []
    x = []
    dates = []
    data_exists = False
    for grind in grinds:
        data_exists = True
        x.append(grind.entry_time)
        #y.append(grind.HS_after)
        y.append(grind.min_diameter)


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








# def rolls_order_now(connection):
#     """Gets a table of rolls whose replacements must be ordered immediately (They are within 
#     a year of needing to be replaced). Query RMS database for rolls that are less than 12 
#     months (1 year) from their approximate scrap date. Put this data in a list and return the
#     list aling with a boolean value representing whether the query was executed successfully 
#     and a connection results message
#     """
#     executed = False
#     query = 'SELECT * FROM roll_new WHERE (approx_scrap_date < DATEADD(year, 1, GETDATE()) \
#         AND approx_scrap_date > GETDATE()) ORDER BY approx_scrap_date;' 
#     cur = connection.cursor()
#     try:
#         cur.execute(query)
#         data = cur.fetchall()
#         table_data = []
#         for row in data:
#             data_row = []
#             for col in range(len(row)):
#                 data_row.append(str(row[col]))
#             table_data.append(data_row)
#         executed = True
#         return table_data, executed, "Database Queried Successfully - Connections.rolls_order_now()"
#     except pp.Error as e:
#         message = "error executing query: " + str(e)
#         return None, executed, message

# def rolls_order_soon(connection):
#     """Gets a table of rolls whose replacements must be ordered soon (They are 12 - 15 
#     months of needing to be replaced). Query RMS database for rolls that are between 12 
#     and 15 months from their approximate scrap date. Put this data in a list and return the
#     list aling with a boolean value representing whether the query was executed successfully 
#     and a connection results message.
#     """
#     executed = False
#     message = ""
#     query = 'SELECT * FROM roll_new WHERE (approx_scrap_date < DATEADD(month, 15, GETDATE())) \
#         AND approx_scrap_date > GETDATE() AND (approx_scrap_date > DATEADD(YEAR, 1, GETDATE())) \
#         ORDER BY approx_scrap_date;'
#     cur = connection.cursor()
#     try:
#         cur.execute(query)
#         data = cur.fetchall()
#         table_data = []
#         for row in data:
#             data_row = []
#             for col in range(len(row)):
#                 data_row.append(str(row[col]))
#             table_data.append(data_row)
#         executed = True
#         return table_data, executed, "Database Queried Successfully - Connections.rolls_order_soon()"
#     except pp.Error as e:
#         message = "error executing query: " + str(e)
#         return None, executed, message
    
# def email_notification_recipients(connection):
#     """Gets a list of the emails registered to receive notification emails from the RMS
#     database. Query the database for the registered employee emails . Put this data in a 
#     list and return the list aling with a boolean value representing whether the query 
#     was executed successfully and a connection results message.
#     """
#     executed = False
#     query = 'SELECT email FROM employee;'
#     cur = connection.cursor()
#     try:
#         cur.execute(query)
#         email_recipients = [employee[0] for employee in cur.fetchall()]
#         executed = True
#         return email_recipients, executed, "Database Queried Successfully - Connections.email_notification_recipients()"
#     except pp.Error as e:
#         message = "error executing query: " + str(e)
#         return None, executed, message





