"""
Python file to predict the lifespan of an aluminum roll for the Kaiser RMS
Written By - Joshua Seward
"""
import pyodbc as pp

# function to get the replacement date for a roll based on a given roll id
def days_until_replacement(roll_id):
    try: # connect to the RMS SQL server database
        connection = pp.connect('Driver= {SQL Server};Server=localhost\\SQLEXPRESS;Database=rms;'
        'uid=rmsapp;pwd=ss1RMSpw@wb02') 
        # cursor for sql query
        cur = connection.cursor()

        # query the database to get the required information to predict the remaining
        # roll life w/ respect to the given roll id
        try:
            cur.execute(f'SELECT r.current_diameter, ri.scrap_diameter, ri.avg_grind_diameter, ri.days_between_rolls'
                         'FROM roll r JOIN roll_info ri ON (r.mill = ri.mill AND r.roll_type = ri.roll_type)'
                         'WHERE r.roll_num = \'%d\';', roll_id)
            # get the matching first row of data and use it to predict the remaining roll life
            query_results = cur.fetchall()
            cur_diameter = float(query_results[0][0])
            scrap_diameter = float(query_results[0][1])
            avg_grind = float(query_results[0][2])
            days_btwn_grinds = float(query_results[0][3])
            remaining_life = remaining_roll_life(cur_diameter, scrap_diameter, avg_grind, days_btwn_grinds)
            # return the calculated remaining roll life
            return remaining_life

        except pp.Error as e: # the SQL query fails
            return str(e)

    except pp.Error as e: # the SQL sdatabase connection fails
        message = "error connecting to SQL Server: " + str(e) #returns error type
        return message

    finally: # close the connection to the database
        connection.close()


# function to predict the number of days remaining before a roll must be 
# scrapped
def remaining_roll_life(cur_diameter, scrap_diameter, avg_grind,
        days_btwn_grinds):
    return ((cur_diameter-scrap_diameter)/avg_grind)*days_btwn_grinds