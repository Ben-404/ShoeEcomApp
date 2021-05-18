# Import Flask
from flask import Flask, render_template, request
# Import SQLite, to interact with database
import sqlite3

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def get_products_brand(brand):
    # If we want shoes from all brands
    if brand == "all":
        query = "SELECT * FROM productdata;"
    # If we want shoes from a specific brand
    else:
        query = "SELECT * FROM productdata WHERE brand='" + brand + "';"

    # Open a connection to the database
    con = sqlite3.connect('static\products.db')

    # Query the database with the SQL statement we set earlier
    cursor = con.execute(query)
    # Retrieve all the products returned by the database
    products = cursor.fetchall()

    # Be sure to close the connection
    con.close()

    return products


@app.route('/home', methods =['GET', 'POST'])
def home():
    # Run the function to retrieve products matching a certain brand
    products = get_products_brand('all')

    # return website and data files
    return render_template('index.html', rows=products)

@app.route('/nike', methods =['GET', 'POST'])
def nike():
    # Run the function to retrieve products matching a certain brand
    products = get_products_brand('Nike')

    # return website and data files
    return render_template('index.html', rows=products)

@app.route('/admin', methods =['GET', 'POST'])
def admin():
    # Run the function to retrieve products matching a certain brand
    products = get_products_brand('all')

    default_name = 'fail'
    data = request.form.get('image-path', default_name)
    print(data)

    # return website and data files
    return render_template('admin.html', rows=products)





if __name__ == '__main__':
	app.run(debug = True)
