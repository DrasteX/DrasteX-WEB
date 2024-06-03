from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

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

            flash('User info updated successfully.', 'success')
        
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

            flash('UI settings updated successfully.', 'success')

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
