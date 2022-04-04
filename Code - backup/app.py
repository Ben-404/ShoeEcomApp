# Import Flask
from flask import Flask, render_template, request, redirect, make_response
# Import SQLite, to interact with database
import sqlite3
# Import my algorithms, statistics and email sender files
import algorithms
import statistics
import emailsender
# Import extra libraries
import json
import requests

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

def update_database(column, productid, value):
    #Connect to sqlite
    conn = sqlite3.connect('static\products.db')

    #Create a cursor object using the cursor() method
    cursor = conn.cursor()

    # Format SQL statement
    sqlstatement = "UPDATE productdata SET "+ column +" = "+ column +" + "+ str(value) +" WHERE productid = " + str(productid)

    # Send the SQL statement to the database
    cursor.execute(sqlstatement)
    
    # Commit the changes to database
    conn.commit()

    # Close connection
    conn.close()

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
    print(sqlstatement)
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

    return products

def edit_product(formdata):
    # Initialise list to hold data for the query
    querydata = []

    # Loop through formdata
    for i in formdata:
        if formdata[i] != '':
            # If value isn't empty, append the data to the list
            querydata.append(str(i + " = '" + formdata[i] + "'"))

    # Preparing SQL queries to UPDATE an existing record in the database
    print(querydata)
    for i in range(1, len(querydata)):
        sqlstatement = "UPDATE productdata SET " + querydata[i] + " WHERE " + querydata[0] + ";"

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
    for i in range(len(homedata[0])):
        sqlstatement += " OR productid LIKE '" + homedata[0][i] + "'"
    
    # Finish off the statement
    sqlstatement += ";"

    # Send the SQL statement to the database
    cursor.execute(sqlstatement)
    
    # Commit the changes to database
    conn.commit()

    # Retrieve all the products returned by the database
    products = cursor.fetchall()




    # Generate an SQL statement to get products by their ID
    sqlstatement = "SELECT * FROM productdata WHERE alert LIKE 'Sale';"

    # Send the SQL statement to the database
    cursor.execute(sqlstatement)
    
    # Commit the changes to database
    conn.commit()

    # Retrieve all the products returned by the database
    saleproducts = cursor.fetchall()


    # Close connection
    conn.close()

    return products, saleproducts

def save_home_products(text, bg_colour, txt_colour, outline_colour):
    data = [
        [
            "1009", 
            "1007",
            "1019",
            "1013"
        ],
        {
            "text": text,
            "bg_colour": bg_colour,
            "txt_colour": txt_colour,
            "outline_colour": outline_colour
        }
    ]

    homedatafile = open("static\homedata.json", "w")
    homedatafile.write(json.dumps(data, indent=4))
    homedatafile.close()

def total_price(products):
    # Loop to work out total price
    total = 0
    for product in products:
        # If product is on sale, use sale price
        if product[5] == 'Sale':
            total += product[6]
        # If not on sale, use normal price
        else:
            total += product[3]
    
    return total

def load_basket_products(cookies):
    product_id_list = []

    # Append the productid of each cookie to a list
    for productid in cookies:
        product_id_list.append(productid)

    # If no items in basket, return empty list and total=0
    if not product_id_list:
        return [], 0

    # Generate an SQL statement to get products by their ID
    sqlstatement = "SELECT * FROM productdata WHERE productid LIKE '" + product_id_list[0] + "'"

    # For each additional product ID, append an extra condition on the SQL statement
    for i in range(1, len(product_id_list)):
        sqlstatement += " OR productid LIKE '" + product_id_list[i] + "'"
    
    # Finish off the statement
    sqlstatement += ";"

    products = call_database(sqlstatement)

    # Call total price function
    total = total_price(products)
        
    return products, total

def edithomebanner(formdata):
    text = formdata["home-txt"]
    bg_colour = formdata["bg-colour"]
    txt_colour = formdata["txt-colour"]
    outline_colour = formdata["outline-colour"]
    
    save_home_products(text, bg_colour, txt_colour, outline_colour)

def get_news():
    # Set API url
    url = 'https://newsapi.org/v2/everything?domains=sneakernews.com&pagesize=4&apiKey=ac97243a35de42a1a73a471b95940193'

    # Make request to API
    news = requests.get(url)
    # Format response data into JSON
    news = news.content
    news = json.loads(news)

    # List to hold data we extract
    news_data = []

    # For each article in API response
    for i in news['articles']:

        # Create a new dict with the data we want
        article = {
            "title": i['title'],
            "description": i['description'],
            'url': i['url'],
            'image': i['urlToImage']
        }
        
        news_data.append(article)
    
    return news_data

@app.route('/v1', methods =['GET', 'POST'])
def version():
    # Run the function to retrieve products matching a certain brand
    products = get_products_brand('all')

    # return website and data files
    return render_template('version.html', rows=products)

@app.route('/home', methods =['GET', 'POST'])
def home():
    products, saleproducts = get_home_products()
    
    # Open JSON file
    f = open('static\homedata.json')

    # Return JSON object as dictionary
    homedata = json.load(f)
    homedata = json.dumps(homedata[1])

    # Close file
    f.close()
    print(homedata)

    # return website and data files
    return render_template('home.html', products=products, saleproducts=saleproducts, homedata=homedata)

@app.route('/all', methods =['GET', 'POST'])
def all():
    # Run the function to retrieve products matching a certain brand
    products = get_products_brand('all')

    statistics.update_traffic()

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
    return render_template('index.html', rows=products, searchquery=searchquery)

# Take parameters from GET request and save as variables
@app.route('/<page>/sort/<sorttype>', methods =['GET'])
def sort(page, sorttype):

    # Get the correct products for the page
    products = get_products_brand(page)

    # Pass these products into the sorting algorithm
    products = algorithms.sort(sorttype, products)

    # return website and data files
    return render_template('index.html', rows=products)

@app.route('/basket', methods =['GET', 'POST'])
def basket():
    # Get all cookies stored in browser
    cookies = request.cookies

    # Pass all cookies into function to retrieve products from database
    products, total = load_basket_products(cookies)

    # return website and data files
    return render_template('basket.html', products=products, total=total)

# When product is added to basket
@app.route('/basket/<int:productid>', methods=['POST'])
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

    update_database('addbasket', productid, 1)

    return resp

# When product is removed from basket
@app.route('/removebasket/<productid>', methods=['GET'])
def remove_from_basket(productid):
    # Save the product id and convert to string
    productid = str(productid)

    resp = make_response(redirect('/basket'))
    # Create a cookie for current productid and set quantity to 1
    resp.set_cookie(productid, '0', max_age=0)

    return resp

# Checkout
@app.route('/checkout', methods =['GET', 'POST'])
def checkout():
    # return website and data files
    return render_template('checkout.html')

# Order confirmed
@app.route('/confirmed', methods =['GET', 'POST'])
def orderconfirmed():
    
    # Recieve formdata sent from checkout page
    if request.method == "POST":
        formdata = request.form

        # Update gender stats
        user_gender = formdata["gender"]
        if user_gender == "male" or user_gender == "female":
            statistics.update_stats("gender", user_gender, 1)
        
        # Update age stats
        user_age = formdata["age"]
        statistics.update_stats("age", user_age, 1)

        # Update user satisfaction
        user_sat = formdata["flexRadioDefault"]
        statistics.update_stats("user_satisfaction", user_sat, 1)

        # Send an order confirmation email using my email sender file
        emailsender.order_confirmation(formdata['email'], formdata['name'], "0281739")
        

    # Get all the products added to basket and convert them to dict
    productdict = request.cookies.to_dict()

    # Begin a list to store product codes for database call
    productslist = []

    # Loop through each product in basket, updating the sales figures in the database
    for product in productdict:
        quantity = productdict.get(product)
        update_database('salecount', product, quantity)
        productslist.append(product)

    # Generate an SQL statement to get products by their ID
    sqlstatement = "SELECT * FROM productdata WHERE productid LIKE '" + productslist[0] + "'"

    # For each additional product ID, append an extra condition on the SQL statement
    for i in range(1, len(productslist)):
        sqlstatement += " OR productid LIKE '" + productslist[i] + "'"
    
    # Finish off the statement
    sqlstatement += ";"

    products = call_database(sqlstatement)

    # Update stats for orders and revenue
    statistics.update_stats("key_stats", "orders", 1)
    statistics.update_stats("key_stats", "revenue", total_price(products))
    # Update sales stats with product brand
    for product in products:
        brand = product[4]
        statistics.update_stats("sales_by_brand", brand, 1)


    # return website and data files
    return render_template('orderconfirmed.html')



@app.route('/admin', methods =['GET', 'POST'])
def admin():
    # Run the function to retrieve products matching a certain brand
    products = get_products_brand('all')

    # Retrieve news data from function
    news_data = get_news()

    if request.method == "POST":
        # Save submitted form data into variable
        formdata = request.form

        # If the forms submit button is named 'addnew'
        if 'addnew' in formdata:
            new_product(formdata)
        # Elif the forms submit button is named 'editexisting'
        elif 'editexisting' in formdata:
            # Run the edit_product function and save output to a variable
            edit_product(formdata)
        elif 'edithomebanner' in formdata:
            edithomebanner(formdata)
        return redirect(request.url)

    admindatafile = open("static/admindata.json", "r")
    admindata = admindatafile.read()
    admindata = json.loads(admindata)
    admindatafile.close()

    # return website and data files
    return render_template('admin.html', rows=products, admindata=admindata, news_data=news_data)


@app.errorhandler(404)
def not_found(e):
  return render_template('error.html'), 404


if __name__ == '__main__':
	app.run(debug = True)
