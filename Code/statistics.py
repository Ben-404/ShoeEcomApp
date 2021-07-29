from app import admin
import json
import sqlite3
import datetime


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
    # Retrieve the number of users who submitted each satisfaction rating
    v_sat = data["very_satisfied"]
    sat = data["satisfied"]
    unsat = data["unsatisfied"]
    v_unset = data["very_unsatisfied"]

    # Save the total number of ratings
    unweight_total = v_sat + sat + unsat + v_unset


    # Multiply the number of users by the weighting for each score
    weight_v_sat = v_sat * 4
    weight_sat = sat * 3
    weight_unsat = unsat * 2
    weight_v_unsat = v_unset * 1

    # Save the total number of weighted ratings
    weight_total = weight_v_sat + weight_sat + weight_unsat + weight_v_unsat

    # Divide the weighted ratings by the number of overall ratings
    score = weight_total / unweight_total
    # Multiply by 2.5 to get a score out of 10
    score = round((score * 2.5), 1)

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



def update_traffic():
    # Open the file containing the admin stats
    admindatafile = open("static/admindata.json", "r+")
    # Read its contents
    admindata = admindatafile.read()

    # Convert contents from JSON to python list
    admindata = json.loads(admindata)

    print(admindata['traffic'])


    for i in range(14):
        print(i)
        day = datetime.datetime.now() - datetime.timedelta(days=i)
        day = day.strftime("%d/%m")
        print(day)

        # Update traffic subdict
        admindata['traffic'][day] = 0


    # Close file
    admindatafile.close()

    print(admindata['traffic'])

    # Reopen the file in write mode, update and close
    admindatafile = open("static/admindata.json", "w")
    admindatafile.write(json.dumps(admindata, indent=4))
    admindatafile.close()