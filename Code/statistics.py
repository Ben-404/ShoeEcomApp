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
def user_sat_score(data):
    # Multiply the number of users by the weighting for each score
    v_sat = (data["very_satisfied"] * 0.4)
    sat = (data["satisfied"] * 0.3)
    unsat = (data["unsatisfied"] * 0.2)
    v_unset = (data["very_unsatisfied"] * 0.1)

    # Add together the weighted scores and divide by 100
    score = (v_sat + sat + unsat + v_unset)
    print(score)
    score = score/10
    print(score)
    # Multiply scores by 2.5 to get a score out of 10, then round it
    score = round((score * 2.5), 1)
    print(score)

    return score
    


def update_stats(subdict, key, value):
    # Open the file containing the admin stats
    admindatafile = open("static/admindata.json", "r+")
    # Read its contents
    admindata = admindatafile.read()

    # Convert contents from JSON to python list
    admindata = json.loads(admindata)
    
    # Update the python list with provided values
    admindata[subdict][key] += value

    if subdict == "user_satisfaction":
        score = user_sat_score(admindata["user_satisfaction"])
        admindata["user_satisfaction"]["score"] = score

    # Close file
    admindatafile.close()

    # Reopen the file in write mode, update and close
    admindatafile = open("static/admindata.json", "w")
    admindatafile.write(json.dumps(admindata, indent=4))
    admindatafile.close()