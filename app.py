from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import json
import os
from werkzeug.utils import secure_filename
import pathlib

Admin_creds = ["tushardesktop1@gmail.com"]



def remove_product(id, anime):
    try:
        with open('/static/JSON/products.json', 'r') as json_file:
            data = json.load(json_file)
    except Exception as E:
        data = {}
    
    data.pop(str(id))
    dirlist = os.listdir(f'{pathlib.Path().resolve()}\\static\\Assets\\MOCKUPS')

    for files in dirlist:
        if f'{anime}_{id}' in files:
            os.remove(f'{pathlib.Path().resolve()}\\static\\Assets\\MOCKUPS\\{files}')
    

    with open('/static/JSON/products.json', 'w') as json_file:
        json.dump(data, json_file, indent = 4)

def add_product(id, name, color, price, instock,  type, anime, m1, m2, m3, m4, m5, m6):
    data_new = {
        "product_name": name,
        "color": color,
        "price": price,
        "in_stock": instock,
        "type":type,
        "anime":anime,
        "mockup1":m1,
        "mockup2":m2,
        "mockup3":m3,
        "mockup4":m4,
        "mockup5":m5,
        "mockup6":m6
    }

    try:
        with open('/static/JSON/products.json', 'r') as json_file:
            data = json.load(json_file)
    except Exception as E:
        data = {}

    data[id] = data_new

    with open('/static/JSON/products.json', 'w') as json_file:
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
                currency TEXT
            )
        ''')
        conn.commit()


# Register route
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

# Login route
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

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('index.html', email=session.get('email'))

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/catalog')
def catalog():
    return render_template('catalog.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/wishlist')
def wishlist():
    return render_template('wishlist.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/orders')
def orders():
    return render_template('orders.html')

@app.route('/add_or_update_products', methods=['GET', 'POST'])
def add_or_update_products():
    if session['email'] not in Admin_creds or 'email' not in session:
        return redirect(url_for('index'))
    
    if request.method=='POST':
        form_type=request.form.get('form_type')

        if form_type == 'delete':
            try:
                with open('/static/JSON/products.json', 'r') as json_file:
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
                with open('/static/JSON/products.json', 'r') as json_file:
                    data = json.load(json_file)
            except Exception as E:
                data = {}
            if id in data:
                flash('A PRODUCT WITH THAT ID ALREADY EXISTS')
                return redirect(url_for('add_or_update_products'))
            else:
                add_product(id, name, color, price, instock,  type, anime, m1fname, m2fname, m3fname, m4fname, m5fname, m6fname)

        return redirect(url_for('add_or_update_products'))
        
    return render_template('add_or_update_products.html')
    
    
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'email' not in session:
        flash('You need to be logged in to access settings.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        
        if form_type == 'user_info':
            street_address = request.form.get('street_address')
            city = request.form.get('city_name')
            state = request.form.get('state_name')
            country = request.form.get('country_name')
            zip_code = request.form.get('zip_code')

            with sqlite3.connect('database.db') as conn:
                c = conn.cursor()
                c.execute('''
                    UPDATE users
                    SET street_address = ?, city = ?, state = ?, country = ?, zip_code = ?
                    WHERE email = ?
                ''', (street_address, city, state, country, zip_code, session['email']))
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
        c.execute('SELECT street_address, city, state, country, zip_code, currency FROM users WHERE email = ?', (session['email'],))
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
        'currency': user[5] if user[5] else 'INR'  # Default to INR if not set
    }

    return render_template('settings.html', user=user_info)

@app.route('/product')
def product():
    return render_template('product.html')




if __name__ == '__main__':
    init_db()
    app.run(debug=True)