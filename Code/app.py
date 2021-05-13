# Import Flask
from flask import Flask, render_template, request
# Import SQLite, to interact with database
import sqlite3

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def get_products_brand(brand):
    # Open a connection to the database
    con = sqlite3.connect('Code\static\products.db')

    # Query the database with an SQL statement
    cursor = con.execute("SELECT * FROM products WHERE brand='" + brand + "';")
    # Retrieve all the products returned by the database
    products = cursor.fetchall()

    # Be sure to close the connection
    con.close()

    return products


@app.route('/home', methods =['GET'])
def home():
    # Run the function to retrieve products matching a certain brand
    products = get_products_brand('Vans')

    # return website and data files
    return render_template('index.html', rows=products)

@app.route('/nike', methods =['GET'])
def nike():
    # Run the function to retrieve products matching a certain brand
    products = get_products_brand('Nike')

    # return website and data files
    return render_template('index.html', rows=products)



if __name__ == '__main__':
	app.run(debug = True)
