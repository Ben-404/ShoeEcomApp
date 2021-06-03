# Import Flask
from flask import Flask, render_template, request, redirect, make_response
# Import SQLite, to interact with database
import sqlite3
# Import my algorithms file
import algorithms
# Import JSON library
import json

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

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

def get_products_brand(brand):
    # Convert capital letters to lowercase
    brand = brand.lower()

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


    # Close the connection
    con.close()

    return products

def new_product(formdata):

    # Get the data we need from the raw form data
    productname = formdata["productname"]
    productid = formdata["productid"]
    brand = formdata["brand"]
    imagepath = formdata["imagepath"]
    normalprice = formdata["normalprice"]
    saleprice =formdata["saleprice"]
    alert = formdata["alert"]

    # Format the formdata ready to be sent to the database
    formdata = [productid, productname, imagepath, normalprice, brand, alert, saleprice]

    # Prepare the string for SQL query
    values = formdata[0]+", '" + formdata[1]+"', '" + formdata[2]+"', " + formdata[3]+", '" + formdata[4]+"', '" + formdata[5]+"', " + formdata[6]
    
    #Connect to sqlite
    conn = sqlite3.connect('static\products.db')

    #Create a cursor object using the cursor() method
    cursor = conn.cursor()

    # Preparing SQL queries to INSERT a record into the database
    sqlstatement = "INSERT INTO productdata(productid, productname, imgname, price, brand, alert, saleprice) VALUES(" + values + ")"
    cursor.execute(sqlstatement)

    # Commit the changes to database
    conn.commit()

    # Close connection
    conn.close()

def search_products(searchquery):

    # Select all records in the database where name contains the search query
    query = "SELECT * FROM productdata WHERE productname LIKE '%" + searchquery + "%' OR brand LIKE '%" + searchquery + "%';"

    # Open a connection to the database
    con = sqlite3.connect('static\products.db')

    # Query the database with the SQL statement we set earlier
    cursor = con.execute(query)
    # Retrieve all the products returned by the database
    products = cursor.fetchall()

    # Close the connection
    con.close()
    print(products)

    return products

def edit_product(formdata):
    # Initialise string to hold data for the query
    querydata = []

    # Loop through formdata
    for i in formdata:
        if formdata[i] != '':
            # If value isn't empty, append the data to the list
            querydata.append(str(i + " = '" + formdata[i] + "'"))

    # Preparing SQL queries to UPDATE an existing record in the database
    for i in range(1, len(querydata)):
        sqlstatement = "UPDATE productdata SET " + querydata[i] + " WHERE " + querydata[0] + ";"
        print(sqlstatement)

    #Connect to sqlite
    conn = sqlite3.connect('static\products.db')

    #Create a cursor object using the cursor() method
    cursor = conn.cursor()

    cursor.execute(sqlstatement)

    # Commit the changes to database
    conn.commit()

    # Close connection
    conn.close()

def get_home_products():
    # Open the file containing the product information for homepage
    homedatafile = open("static\homedata.json", "r")
    # Read its contents
    homedata = homedatafile.read()

    # Convert contents from JSON to python list
    homedata = json.loads(homedata)
    # Close file
    homedatafile.close()

    #Connect to sqlite
    conn = sqlite3.connect('static\products.db')

    #Create a cursor object using the cursor() method
    cursor = conn.cursor()

    # Generate an SQL statement to get products by their ID
    sqlstatement = "SELECT * FROM productdata WHERE productid LIKE '" + homedata[0][0] + "'"

    # For each additional product ID, append an extra condition on the SQL statement
    for i in range(1, len(homedata[0])):
        sqlstatement += " OR productid LIKE '" + homedata[0][i] + "'"
    
    # Finish off the statement
    sqlstatement += ";"

    # Send the SQL statement to the database
    cursor.execute(sqlstatement)
    
    # Commit the changes to database
    conn.commit()

    # Retrieve all the products returned by the database
    products = cursor.fetchall()

    # Close connection
    conn.close()

    # Save the extra information from the JSON
    saleon = homedata[1]["saleon"]
    saleimage = homedata[1]["saleimage"]

    return products, saleon, saleimage

def save_home_products():
    data = [
        [
            "1009", 
            "1007",
            "1019",
            "1013"
        ],
        {
            "saleon": "true",
            "saleimage": "static\\images\\nikesale.png"
        }
    ]

    homedatafile = open("static\homedata.json", "w")
    homedatafile.write(json.dumps(data, indent=4))
    homedatafile.close()

def load_basket_products(cookies):
    product_id_list = []

    # Append the productid of each cookie to a list
    for productid in cookies:
        product_id_list.append(productid)
    print(product_id_list)

    # Generate an SQL statement to get products by their ID
    sqlstatement = "SELECT * FROM productdata WHERE productid LIKE '" + product_id_list[1] + "'"

    # For each additional product ID, append an extra condition on the SQL statement
    for i in range(1, len(product_id_list)):
        sqlstatement += " OR productid LIKE '" + product_id_list[i] + "'"
    
    # Finish off the statement
    sqlstatement += ";"

    call_database


@app.route('/home', methods =['GET', 'POST'])
def home():
    save_home_products()

    products, saleon, saleimage = get_home_products()

    # return website and data files
    return render_template('home.html', products=products, saleon=saleon, saleimage=saleimage)

@app.route('/all', methods =['GET', 'POST'])
def all():
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

@app.route('/adidas', methods =['GET', 'POST'])
def adidas():
    # Run the function to retrieve products matching a certain brand
    products = get_products_brand('adidas')

    # return website and data files
    return render_template('index.html', rows=products)

@app.route('/vans', methods =['GET', 'POST'])
def vans():
    # Run the function to retrieve products matching a certain brand
    products = get_products_brand('Vans')

    # return website and data files
    return render_template('index.html', rows=products)

@app.route('/converse', methods =['GET', 'POST'])
def converse():
    # Run the function to retrieve products matching a certain brand
    products = get_products_brand('Converse')

    # return website and data files
    return render_template('index.html', rows=products)


@app.route('/search', methods =['GET', 'POST'])
def searchresults():

    if request.method == "POST":
        searchquery = request.form
        searchquery = searchquery['search']
        
        # Run the function to search the database
        products = search_products(searchquery)

    # return website and data files
    return render_template('index.html', rows=products)

# Take parameters from GET request and save as variables
@app.route('/<page>/sort/<sorttype>', methods =['GET'])
def sort(page, sorttype):

    # Get the correct products for the page
    products = get_products_brand(page)

    # Pass these products into the sorting algorithm
    products = algorithms.sort(sorttype, products)

    # return website and data files
    return render_template('index.html', rows=products)

@app.route('/basket', methods =['GET'])
def basket():
    # Get all cookies stored in browser
    cookies = request.cookies

    # Pass all cookies into function to retrieve products from database
    load_basket_products(cookies)

    # return website and data files
    return render_template('basket.html')

# When product is added to basket
@app.route('/basket/<productid>', methods=['POST'])
def add_to_basket(productid):
    # Save the product id and convert to string
    productid = str(productid)
    # Retrieve the quantity 
    current_quantity = str(request.cookies.get(productid))

    # If there is no cookie for current productid
    if current_quantity == 'None':
        resp = make_response(redirect(request.url))
        # Create a cookie for current productid and set quantity to 1
        resp.set_cookie(productid, '1')

    # If there is already a cookie for current productid
    else:
        # Convert quantity to int and add 1
        current_quantity = int(current_quantity)
        current_quantity += 1

        # Configure the response
        resp = make_response(redirect(request.url))
        resp.set_cookie(productid, str(current_quantity))

    return resp

@app.route('/admin', methods =['GET', 'POST'])
def admin():
    # Run the function to retrieve products matching a certain brand
    products = get_products_brand('all')

    if request.method == "POST":
        # Save submitted form data into variable
        formdata = request.form

        # If the forms submit button is named 'addnew'
        if 'addnew' in formdata:
            new_product(formdata)
        # Elif the forms submit button is named 'editexisting'
        elif 'editexisting' in formdata:
            print(formdata)
            # Run the edit_product function and save output to a variable
            edit_product(formdata)
        return redirect(request.url)

    # return website and data files
    return render_template('admin.html', rows=products)





if __name__ == '__main__':
	app.run(debug = True)
