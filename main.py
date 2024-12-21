# from flask import Flask,redirect,url_for,render_template, request, flash 
import re
import random
import time
from flask import Flask, request, jsonify, render_template, session, flash, redirect, url_for
from flask_mail import Mail, Message
import sqlite3
# from flask_sqlalchemy import SQLAlchemy
# import pymysql
app = Flask(__name__)
app.secret_key = 'mysecrethifi'
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            location TEXT,
            contact TEXT
        )
    """)
    # Contact messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'hifidelivery213@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'oiya zlhv irvc yowz'  # Replace with your app-specific password

mail = Mail(app)
# Store OTPs in memory (can be changed to a database in production)
otp_store = {}

# Send OTP to the email
def send_otp(email, otp):
    try:
        msg = Message('Your OTP Code', sender=app.config['MAIL_USERNAME'], recipients=[email])
        msg.body = f"Your OTP code is {otp}. It will expire in 10 minutes."
        mail.send(msg)
        print(f"OTP sent to {email}")
    except Exception as e:
        print(f"Error sending OTP: {e}")
        return False
    return True

@app.route('/home') 
def start():
    return render_template('homepage.html')

@app.route('/send_otp', methods=['POST'])
def send_otp_route():
    data = request.get_json()
    email = data.get('email')

    if not email or not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        return jsonify({'success': False, 'message': 'Invalid email format.'})

    otp = str(random.randint(100000, 999999))
    otp_store[email] = {'otp': otp, 'timestamp': time.time()}  # Store OTP with timestamp

    if send_otp(email, otp):
        return jsonify({'success': True, 'message': 'OTP sent to email.'})
    else:
        return jsonify({'success': False, 'message': 'Error sending OTP.'})

@app.route('/',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM users WHERE username = ? AND password = ?
            """, (username, password))
            user = cursor.fetchone()

            if user:
                if username == "admin" and password == "123456":
                    flash('Login successful! Welcome back, Admin.', 'success')
                    return redirect(url_for('admin'))  # Redirect to admin dashboard
                else:
                    role = user['role']  # Get the user's role
                    if role == 'Customer':
                        flash('Login successful! Welcome back, Customer.', 'success')
                        return redirect(url_for('start'))  # Redirect to customer dashboard
                    elif role == 'Agent':
                        flash('Login successful! Welcome back, Agent.', 'success')
                        return redirect(url_for('delivery'))  # Redirect to agent dashboard
                # elif role == 'Admin':
                #     flash('Login successful! Welcome back, Admin.', 'success')
                #     return redirect(url_for('admin'))  # Redirect to admin dashboard
            else:
                flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')

def get_db_connection():
    conn = sqlite3.connect('database.db', timeout=10)  # Timeout to avoid lock
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        role = request.form['role']
        location = request.form['location']
        contact = request.form['contact']

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (username, password, email, role, location, contact)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (username, password, email, role, location, contact))
                conn.commit()

            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.OperationalError:
            flash('Database is currently locked. Please try again later.', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html')  # Ensure register.html is your registration page

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Save the contact message to the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO contact_messages (name, email, message)
            VALUES (?, ?, ?)
        ''', (name, email, message))
        conn.commit()
        conn.close()

        flash("Message sent successfully!", "success")
        return redirect(url_for('contact'))

    return render_template('contact.html')

@app.route('/forgot')
def forgot():
    return render_template('forgot.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/delivery')
def delivery():
    return render_template('delivery.html')

@app.route('/recovery')
def recovery():
    return render_template('recovery.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')


# @app.route('/verify_data', methods=['GET', 'POST'])
# def verify_data():
#     print("Verify data function triggered.")  # Debugging line
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         repassword = request.form['repassword']
#         email = request.form['email']
#         phone = request.form['phone']
#         otp = request.form['otp']
#         print(f'username : {username}\npassword:{password}\nrepassword:{repassword}\nemail:{email}\nphone:{phone}\notp:{otp}')


        # print(f"Username: {username}, Email: {email}")  # Check if values are correct
        
        # # Check if user already exists
        # existing_user = User.query.filter_by(email=email).first()
        # if existing_user:
        #     flash('Email already registered. Please use a different one.', 'warning')
        #     return redirect(url_for('register'))
        
        # # Check if password and confirm password match
        # if password != confirm_password:
        #     flash('Passwords do not match. Please try again.', 'danger')
        #     return redirect(url_for('register'))
        
        # # Debugging before attempting to add the user
        # print("Attempting to add new user to the database.")

        # if len(password) < 6:
        #     flash("Password must be at least 6 characters long.", "error")
        #     return redirect(url_for('register'))
        
        # if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        #     flash("Invalid email format.", "error")
        #     return redirect(url_for('register'))
        
        # if not re.match(r'^\d{10}$', phone):
        #     flash("Contact number must be a valid 10-digit number.", "error")
        #     return redirect(url_for('register'))

    
        # # Save new user to the database
        # new_user = User(username=username, email=email, location=location, contact=contact, password=password)
        # try:
        #     db.session.add(new_user)
        #     db.session.commit()
        #     flash('Registration successful! Please log in.', 'success')
        #     return redirect(url_for('login'))
        # except Exception as e:
        #     db.session.rollback()
        #     flash(f'Error: {e}', 'danger')
        #     return redirect(url_for('register'))
         
    # return redirect(url_for('start'))


# @app.route('/verify_login_data',methods=['GET','POST'])
# def verify_login_data():
#     choice = 'start'
#     if request.method == 'POST':
#         identifier = request.form['identifier']
#         password = request.form['password']
#         repassword = request.form['repassword']
#         role = request.form['type']
#         print(f'identifier:{identifier}\npassword:{password}\nrepassword:{repassword}\nrole:{role}')
#         if role == 'customer':
#             choice = 'start'
#         elif role == 'admin':
#             choice = 'admin'
#         else:
#             choice = 'delivery'
#     return redirect(url_for(choice))
            
        

# @app.route('/submit_contact',methods=['GET','POST'])
# def submit_contact():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         message = request.form['message']
#         print(f'name:{name}\nemail:{email}\nmessage:{message}')
#         if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
#             flash("Invalid email format.", "error")
#             return redirect(url_for('register'))
#     return redirect(url_for('start'))
    

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        identifier = request.form.get('identifier')
        new_password = request.form.get('new_password')
        re_new_password = request.form.get('re_new_password')
        print(f'identifier:{identifier}\nnew_password:{new_password}\nre-new-password:{re_new_password}')


        if new_password != re_new_password:
            flash('Passwords do not match. Please try again.', 'error')
            return redirect(url_for('forgot_password'))


        flash('Password reset successful. Please log in with your new password.', 'success')
        return redirect(url_for('start'))

    return render_template(url_for('forgot'))

@app.route('/submit_profile', methods=['GET', 'POST'])
def submit_profile():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        location = request.form['location']
        print(name,email,phone,location,sep='\n')
        return redirect(url_for('start'))

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()  #create tables if they don't exists
    app.run(debug=True)



