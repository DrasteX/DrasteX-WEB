from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import json
import os
from werkzeug.utils import secure_filename
import pathlib 
import requests






Admin_creds = ["tushardesktop1@gmail.com"]
QIKINK_CLIENT_ID = "323252398360424"
QIKINK_CLIENT_SECRET = "5537d032b1ea68004b61e712ca5e89468633be92dbc0fc725be7d9061555ee51"
RAZORPAY_KEY_ID = "rzp_test_pck2VeZ7ka4SzX"
RAZORPAY_KEY_SECRET = "gj1BNaaLLTqURwFonbkJYGt6"

def getaccesstoken():
    url = "https://sandbox.qikink.com/api/token"

    payload=f'ClientId={QIKINK_CLIENT_ID}&client_secret={QIKINK_CLIENT_SECRET}'
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text
print(getaccesstoken())
def joinList(list, sep):
    result = ''
    for items in list:
        result += str(items)
        if list.index(items) != len(list)-1:
            result+=sep
    return result
    
def addToCart_fn(email, id, color, size):
    try:
        with open(f'{pathlib.Path().resolve()}/static/JSON/user_products_info.json', 'r') as json_file:
            data = json.load(json_file)
    except Exception as E:
        data = {}

    # Ensure user data exists
    if email not in data:
        data[email] = {"cart": {}}

    # Ensure cart data exists
    if "cart" not in data[email]:
        data[email]["cart"] = {}

    # Add or update product in cart
    if f'{id}_{size}' in data[email]['cart']:
        # If the item already exists, update its details
        data[email]['cart'][f'{id}_{size}']['quantity'] += 1
        data[email]['cart'][f'{id}_{size}']['size'] = size
        data[email]['cart'][f'{id}_{size}']['color'] = color
    else:
        # If the item does not exist, add it to the cart
        data[email]['cart'][f'{id}_{size}'] = {
            "quantity": 1,
            "size": size,
            "color": color
        }

    # Save the updated data back to the JSON file
    with open(f'{pathlib.Path().resolve()}/static/JSON/user_products_info.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

def remove_product(id, anime):
    try:
        with open(f'{pathlib.Path().resolve()}/static/JSON/products.json', 'r') as json_file:
            data = json.load(json_file)
    except Exception as E:
        data = {}
    
    data.pop(str(id))
    dirlist = os.listdir(f'{pathlib.Path().resolve()}\\static\\Assets\\MOCKUPS')

    for files in dirlist:
        if f'{anime}_{id}' in files:
            os.remove(f'{pathlib.Path().resolve()}\\static\\Assets\\MOCKUPS\\{files}')
    

    with open(f'{pathlib.Path().resolve()}/static/JSON/products.json', 'w') as json_file:
        json.dump(data, json_file, indent = 4)

def add_product(id, name, color, price, instock,  type, anime,sku, m1, m2, m3, m4, m5, m6):
    data_new = {
        "product_name": name,
        "color": color,
        "price": price,
        "in_stock": bool(instock),
        "type":type,
        "anime":anime,
        "sku":sku,
        "mockup1":m1,
        "mockup2":m2,
        "mockup3":m3,
        "mockup4":m4,
        "mockup5":m5,
        "mockup6":m6
    }

    try:
        with open(f'{pathlib.Path().resolve()}/static/JSON/products.json', 'r') as json_file:
            data = json.load(json_file)
    except Exception as E:
        data = {}

    data[id] = data_new

    with open(f'{pathlib.Path().resolve()}/static/JSON/products.json', 'w') as json_file:
        json.dump(data, json_file, indent = 4)



app = Flask(__name__)
app.secret_key = 'dev'

def init_db():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                street_address TEXT,
                city TEXT,
                state TEXT,
                country TEXT,
                zip_code TEXT,
                phone_number TEXT,
                fname TEXT,
                lname TEXT,
                currency TEXT
            )
        ''')
        conn.commit()

# INDEX
@app.route('/')
def index():
    return render_template('index.html', email=session.get('email'))

# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'message')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            try:
                c.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_password))
                conn.commit()
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash('Email already exists. Please choose another.', 'message')

    return render_template('register.html')

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM users WHERE email = ?', (email,))
            user = c.fetchone()

            if user and check_password_hash(user[2], password):
                session['user_id'] = user[0]
                session['email'] = user[1]
                return redirect(url_for('index'))
            else:
                flash('Invalid email or password.', 'message')

    return render_template('login.html')

# LOGOUT
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('email', None)
    return redirect(url_for('index'))

# SETTINGS
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'email' not in session:
        flash('You need to be logged in to access settings.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        
        if form_type == 'user_info':
            fname = request.form.get('fname')
            lname = request.form.get('lname')
            phone_number = request.form.get('phone_number')
            street_address = request.form.get('street_address')
            city = request.form.get('city_name')
            state = request.form.get('state_name')
            country = request.form.get('country_name')
            zip_code = request.form.get('zip_code')

            with sqlite3.connect('database.db') as conn:
                c = conn.cursor()
                c.execute('''
                    UPDATE users
                    SET street_address = ?, city = ?, state = ?, country = ?, zip_code = ?, phone_number = ?, fname = ?, lname = ?
                    WHERE email = ?
                ''', (street_address, city, state, country, zip_code, phone_number, fname, lname, session['email']))
                conn.commit()
        
        elif form_type == 'ui_settings':
            currency = request.form.get('currency')

            with sqlite3.connect('database.db') as conn:
                c = conn.cursor()
                c.execute('''
                    UPDATE users
                    SET currency = ?
                    WHERE email = ?
                ''', (currency, session['email']))
                conn.commit()

        return redirect(url_for('settings'))
    
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('SELECT street_address, city, state, country, zip_code, phone_number, fname, lname, currency FROM users WHERE email = ?', (session['email'],))
        user = c.fetchone()

    if user is None:
        flash('User not found.', 'error')
        return redirect(url_for('index'))

    user_info = {
        'street_address': user[0] if user[0] else '',
        'city': user[1] if user[1] else '',
        'state': user[2] if user[2] else '',
        'country': user[3] if user[3] else '',
        'zip_code': user[4] if user[4] else '',
        'phone_number': user[5] if user[5] else '',
        'fname' : user[6] if user[6] else '',
        'lname' : user[7] if user[7] else '',
        'currency': user[8] if user[8] else 'INR'  # Default to INR if not set
    }

    return render_template('settings.html', user=user_info)

# PRODUCT PAGE
@app.route('/product')
def product():
    return render_template('product.html')

# CONTACT
@app.route('/contact')
def contact():
    return render_template('contact.html')

# CATALOG
@app.route('/catalog')
def catalog():
    return render_template('catalog.html')

# WISHLIST
@app.route('/wishlist')
def wishlist():
    return render_template('wishlist.html')

# CART
@app.route('/cart', methods=['POST','GET'])
def cart():
    return render_template('cart.html', email=session['email'])

# ORDERS
@app.route('/orders')
def orders():
    return render_template('orders.html')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'email' not in session:
        flash('You need to be logged in to order.', 'error')
        return redirect(url_for('login'))
    if request.method == "POST":

        fname = request.form.get('fname').capitalize()
        lname = request.form.get('lname').capitalize()
        phone = request.form.get('phone')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state').capitalize()
        zip = request.form.get('zip')
        country = request.form.get('country').upper()

        product_id = request.args.get('product_id')
        order_type = request.args.get('order_type')

        create_order(fname,lname,address,phone,city,zip,state,country, product_id, order_type)



    with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('SELECT street_address, city, state, country, zip_code, phone_number, fname, lname, currency FROM users WHERE email = ?', (session['email'],))
            user = c.fetchone()

    if user is None:
        flash('User not found.', 'error')
        return redirect(url_for('index'))


    user_info = {
        'street_address': user[0] if user[0] else '',
        'city': user[1] if user[1] else '',
        'state': user[2] if user[2] else '',
        'country': user[3] if user[3] else '',
        'zip_code': user[4] if user[4] else '',
        'phone_number': user[5] if user[5] else '',
        'fname' : user[6] if user[6] else '',
        'lname' : user[7] if user[7] else '',
        'currency': user[8] if user[8] else 'INR'  # Default to INR if not set
    }

    return render_template('checkout.html', user=user_info)

@app.route('/add_or_update_products', methods=['GET', 'POST'])
def add_or_update_products():
    if session['email'] not in Admin_creds or 'email' not in session:
        return redirect(url_for('index'))
    
    if request.method=='POST':
        form_type=request.form.get('form_type')

        if form_type == 'delete':
            try:
                with open(f'{pathlib.Path().resolve()}/static/JSON/products.json', 'r') as json_file:
                    data = json.load(json_file)
            except Exception as E:
                data = {}

            id = request.form.get('product_id')
            anime = data[id]['anime']
            if id in data:
                remove_product(str(id), anime)
            else:
                flash('A PRODUCT WITH THAT ID DOESNT EXISTS')
                return redirect(url_for('add_or_update_products'))
        elif form_type == 'add':
            id = request.form.get('product_id')
            name = request.form.get('product_name')
            price= request.form.get('product_price')
            color = request.form.get('product_color')
            type = request.form.get('product_type')
            anime = request.form.get('product_anime')
            instock = request.form.get('product_instock')
            sku = request.form.get('sku')

            m1 = request.files['mockup1']
            m1fname = f'Assets/MOCKUPS/{anime}_{id}_1.{m1.filename.split('.')[-1]}'
            m1.save(f'{pathlib.Path().resolve()}\\static\\Assets\\MOCKUPS\\{anime}_{id}_1.{m1.filename.split('.')[-1]}')

            m2 = request.files['mockup2']
            m2fname = f'Assets/MOCKUPS/{anime}_{id}_2.{m2.filename.split('.')[-1]}'
            m2.save(f'{pathlib.Path().resolve()}\\static\\Assets\\MOCKUPS\\{anime}_{id}_2.{m2.filename.split('.')[-1]}')

            m3 = request.files['mockup3']
            m3fname = f'Assets/MOCKUPS/{anime}_{id}_3.{m3.filename.split('.')[-1]}'
            m3.save(f'{pathlib.Path().resolve()}\\static\\Assets\\MOCKUPS\\{anime}_{id}_3.{m3.filename.split('.')[-1]}')

            m4 = request.files['mockup4']
            m4fname = f'Assets/MOCKUPS/{anime}_{id}_4.{m4.filename.split('.')[-1]}'
            m4.save(f'{pathlib.Path().resolve()}\\static\\Assets\\MOCKUPS\\{anime}_{id}_4.{m4.filename.split('.')[-1]}')

            m5 = request.files['mockup5']
            m5fname = f'Assets/MOCKUPS/{anime}_{id}_5.{m5.filename.split('.')[-1]}'
            m5.save(f'{pathlib.Path().resolve()}\\static\\Assets\\MOCKUPS\\{anime}_{id}_5.{m5.filename.split('.')[-1]}')

            m6 = request.files['mockup6']
            m6fname = f'Assets/MOCKUPS/{anime}_{id}_6.{m6.filename.split('.')[-1]}'
            m6.save(f'{pathlib.Path().resolve()}\\static\\Assets\\MOCKUPS\\{anime}_{id}_6.{m6.filename.split('.')[-1]}')
        
            try:
                with open(f'{pathlib.Path().resolve()}/static/JSON/products.json', 'r') as json_file:
                    data = json.load(json_file)
            except Exception as E:
                data = {}
            if id in data:
                flash('A PRODUCT WITH THAT ID ALREADY EXISTS')
                return redirect(url_for('add_or_update_products'))
            else:
                add_product(id, name, color, price, instock,  type, anime, sku, m1fname, m2fname, m3fname, m4fname, m5fname, m6fname)

        return redirect(url_for('add_or_update_products'))
        
    return render_template('add_or_update_products.html')
    





# NO HTML ROUTES

@app.route('/update_cart', methods=['POST'])
def update_cart():
    dataget = request.json
    email = session['email']
    id = dataget['id']
    quantity = int(dataget['quantity'])

    try:
        with open(f'{pathlib.Path().resolve()}/static/JSON/user_products_info.json', 'r') as json_file:
            data = json.load(json_file)
    except Exception as E:
        data = {}
    print(email, id, quantity)
    data[email]['cart'][id]['quantity'] = quantity
    if quantity < 1:
        del data[email]['cart'][id]

    with open(f'{pathlib.Path().resolve()}/static/JSON/user_products_info.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    return jsonify({'status': 'success'})

@app.route('/addtocart', methods=['POST', 'GET'])
def addtocart():
    if 'email' not in session:
        flash('You need to be logged in to add items to the cart.', 'error')
        return redirect(url_for('login'))

    product_id = request.args.get('product_id')
    color = request.args.get('color')
    size = request.args.get('size')

    addToCart_fn(session['email'], product_id, color, size)
    return redirect(url_for('cart'))

def create_order(fname, lname, address, phone,city, zip, province, country, product_id, order_type):
    user_email = session.get('email')

    payload = {
        "order_number": "",
        "qikink_shipping": "1",
        "gateway": "Prepaid",
        "total_order_value": "",
        "line_items": [
            {
                "search_from_my_products": 1,
                "quantity": "1",
                "price":"1",
                "sku": "MVnHs-Wh-S",
            }
        ],
        "shipping_address": {
            "first_name": "",
            "last_name": "",
            "address1": "",
            "phone":"",
            "email": "",
            "city":"",
            "zip":"",
            "province":"",
            "country_code":"IN"
        }
    }
    
    

    # TOTAL ORDER VALUE
    total_order_value = request.args.get('tval')
    payload["total_order_value"] = total_order_value

    # ORDER NUMBER
    with open(f'{pathlib.Path().resolve()}/static/JSON/website_stats.json', 'r') as file:
        data = json.load(file)
    order_number = data["no_of_orders"] + 1
    payload["order_number"] = order_number

    # CUSTOMER DETAILS
    payload["shipping_address"]["first_name"] = fname
    payload["shipping_address"]["last_name"] = lname
    payload["shipping_address"]["address1"] = address
    payload["shipping_address"]["phone"] = phone
    payload["shipping_address"]["email"] = session.get('email')
    payload["shipping_address"]["city"] = city
    payload["shipping_address"]["zip"] = zip
    payload["shipping_address"]["province"] = province
    payload["shipping_address"]["country_code"] = country


    if order_type == "0":
        with open(f'{pathlib.Path().resolve()}/static/JSON/products.json', 'r') as file:
            data = json.load(file)
        item_price = data[product_id]['price']
        item_sku = data[product_id]['sku'][request.args.get('size')]
        payload["line_items"] = [{
            "search_from_my_products": 1,
            "quantity": "1",
            "price":item_price,
            "sku": item_sku,
        }]
    elif order_type == "1":
        payload["line_items"] = []
        with open(f'{pathlib.Path().resolve()}/static/JSON/user_products_info.json', 'r') as file:
            userproducts_data = json.load(file)
        with open(f'{pathlib.Path().resolve()}/static/JSON/products.json', 'r') as file:
            siteproducts_data = json.load(file)
        usercart = userproducts_data[user_email]['cart']
        for items in usercart:
            product_id = items.split('_')[0]
            size = items.split('_')[1]
            base_sku = siteproducts_data[product_id]['sku']
            base_sku = base_sku.split('-')
            base_sku[2] = size.upper()
            item_sku = joinList(base_sku, '-')
            product_info = {
               "search_from_my_products": 1, 
               "quantity": usercart[items]['quantity'],
               "price": siteproducts_data[product_id]['price'],
               "sku": item_sku
            }
            payload["line_items"].append(product_info)

    print(payload)
        



    
    url = "https://sandbox.qikink.com/api/order/create"

    
    headers = {
        'ClientId': QIKINK_CLIENT_ID,
        'Accesstoken': QIKINK_ACCESS_TOKEN
    }

    json_payload = json.dumps(payload, indent=4)
    raw_payload = json_payload.replace('\n', '\\r\\n').replace('"', '\\"')
    payload = f'"{raw_payload}"'
    payload = "{\r\n    \"order_number\": \"1050\",\r\n    \"qikink_shipping\": \"0\",\r\n    \"gateway\": \"COD\",\r\n    \"total_order_value\": \"1\",\r\n    \"line_items\": [\r\n        {\r\n            \"search_from_my_products\": 0,\r\n            \"quantity\": \"1\",\r\n            \"price\":\"1\",\r\n            \"sku\": \"MVnHs-Wh-S\",\r\n            \"designs\": [\r\n                {\r\n                    \"design_code\": \"123\",\r\n                    \"width_inches\": \"\",\r\n                    \"height_inches\": \"\",\r\n                    \"placement_sku\": \"fr\",\r\n                    \"design_link\":\"\"\r\n                }\r\n            ]\r\n        }\r\n    ],\r\n    \"shipping_address\": {\r\n        \"first_name\": \"sdf\",\r\n        \"last_name\": \"ds\",\r\n        \"address1\": \"sdsfsdf3\",\r\n        \"phone\":\"fasda\",\r\n        \"email\": \"adf\",\r\n        \"city\":\"sda\",\r\n        \"zip\":\"sdfs\",\r\n        \"province\":\"sdfa\",\r\n        \"country_code\":\"IN\"\r\n    }\r\n}"

    
    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)




if __name__ == '__main__':
    init_db()
    app.run(debug=True)