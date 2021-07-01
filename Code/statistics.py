import json
import sqlite3


def call_database(sqlstatement):
    #Connect to sqlite
    conn = sqlite3.connect('static\products.db')

    #Create a cursor object using the cursor() method
    cursor = conn.cursor()

    # Send the SQL statement to the database
    cursor.execute(sqlstatement)
    
    # Commit the changes to database
    conn.commit()

    # Retrieve all the products returned by the database
    database_response = cursor.fetchall()

    # Close connection
    conn.close()

    return database_response

"""
# This function is called by main.py to return the statistics for admin panel
def get_stats():
    sqlstatement = 'SELECT SUM(addbasket) FROM productdata;'
    basketcount = 12 #call_database(sqlstatement)
    sqlstatement = 'SELECT SUM(salecount) FROM productdata;'
    salecount = 32 #call_database(sqlstatement)

    
    purchase_completion_brand = [32, 56, 73, 13]

    
"""

def update_stats(subdict, key, value):
    # Open the file containing the admin stats
    admindatafile = open("static/admindata.json", "r+")
    # Read its contents
    admindata = admindatafile.read()

    # Convert contents from JSON to python list
    admindata = json.loads(admindata)
    
    # Update the python list with provided values
    admindata[subdict][key] += value

    # Close file
    admindatafile.close()

    # Reopen the file in write mode, update and close
    admindatafile = open("static/admindata.json", "w")
    admindatafile.write(json.dumps(admindata, indent=4))
    admindatafile.close()

update_stats("key_stats", "orders", 1)