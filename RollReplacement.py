"""
Python file to predict the lifespan of an aluminum roll for the Kaiser RMS
Written By - Joshua Seward
"""
import pyodbc as pp

# function to get the replacement date for a roll based on a given roll id
def roll_replacement_date(roll_id):
    # connect to the RMS SQL server database
    try:
        connection = pp.connect('Driver= {SQL Server};Server=localhost\\SQLEXPRESS;Database=rms;'
        'uid=rmsapp;pwd=ss1RMSpw@wb02') 
    except pp.Error as e:
        message = "error connecting to SQL Server: " + str(e) #returns error type
        return message
    return

# function to predict the number of days remaining before a roll must be 
# scrapped
def remaining_roll_life(cur_diameter, scrap_diameter, avg_grind,
        days_btwn_grinds):
    return ((cur_diameter-scrap_diameter)/avg_grind)*days_btwn_grinds