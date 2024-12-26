# from flask import Flask,redirect,url_for,render_template, request, flash 
# import re
# from flask import Flask, render_template, request, redirect, url_for, flash, session
# from werkzeug.security import generate_password_hash, check_password_hash
# import sqlite3
# # from database_setup import init_db


# app = Flask(__name__)
# app.secret_key = 'mysecrethifi'
# # Initialize the database
# def init_db():
#     conn = sqlite3.connect("database.db")
#     cursor = conn.cursor()
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT,
#             username TEXT NOT NULL UNIQUE,
#             email TEXT NOT NULL UNIQUE,
#             password TEXT NOT NULL,
#             role TEXT NOT NULL,
#             location TEXT,
#             contact TEXT
#         )
#     """)
#     # Contact messages table
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS contact_messages (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             email TEXT NOT NULL,
#             message TEXT NOT NULL
#         )
#     ''')
#     conn.commit()
#     conn.close()


# init_db()

# @app.route('/',methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         with get_db_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute("""
#                 SELECT * FROM users WHERE username = ? AND password = ?
#             """, (username, password))
#             user = cursor.fetchone()

#             if user:
#                 if username == "admin" and password == "123456":
#                     flash('Login successful! Welcome back, Admin.', 'success')
#                     return redirect(url_for('admin'))  # Redirect to admin dashboard
#                 else:
#                     role = user['role']  # Get the user's role
#                     if role == 'Customer':
#                         flash('Login successful! Welcome back, Customer.', 'success')
#                         return redirect(url_for('start'))  # Redirect to customer dashboard
#                     elif role == 'Agent':
#                         flash('Login successful! Welcome back, Agent.', 'success')
#                         return redirect(url_for('delivery'))  # Redirect to agent dashboard
#                 # elif role == 'Admin':
#                 #     flash('Login successful! Welcome back, Admin.', 'success')
#                 #     return redirect(url_for('admin'))  # Redirect to admin dashboard
#             else:
#                 flash('Invalid username or password. Please try again.', 'danger')

#     return render_template('login.html')

# @app.route('/home')
# def start():
#     return render_template("homepage.html")

# @app.route('/admin')
# def admin():
#     return render_template('admin.html')

# @app.route('/delivery')
# def delivery():
#     return render_template('deliveryagent.html')

# @app.route('/user-profile')
# def profile():
#     return render_template("profile.html")

# @app.route('/passrecover')
# def recover():
#     return render_template("recovery.html")

# @app.route('/info')
# def info():
#     return render_template("info.html")

# # @app.route('/contact')
# # Contact Route (example)
# @app.route('/contact', methods=['GET', 'POST'])
# def contact():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         message = request.form['message']

#         # Save the contact message to the database
#         conn = sqlite3.connect('database.db')
#         cursor = conn.cursor()
#         cursor.execute('''
#             INSERT INTO contact_messages (name, email, message)
#             VALUES (?, ?, ?)
#         ''', (name, email, message))
#         conn.commit()
#         conn.close()

#         flash("Message sent successfully!", "success")
#         return redirect(url_for('contact'))

#     return render_template('contact.html')

# @app.route('/profile', methods=['GET', 'POST'])
# def profile_update():
#     if 'user_id' not in session:
#         flash('You must be logged in to view your profile', 'danger')
#         return redirect(url_for('login'))  # Redirect to login page if not logged in

#     user_id = session['user_id']  # Assuming you store user ID in session after login

#     if request.method == 'GET':
#         # Fetch user details from the database
#         with get_db_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
#             user = cursor.fetchone()

#         if user:
#             # Pass user data to the template
#             return render_template('profile.html', user=user)
#         else:
#             flash('User not found', 'danger')
#             return redirect(url_for('login'))

#     if request.method == 'POST':
#         # Get the updated details from the form
#         name = request.form['name']
#         email = request.form['email']
#         phone = request.form['phone']
#         location = request.form['location']

#         # Update the user details in the database
#         with get_db_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute("""
#                 UPDATE users
#                 SET name = ?, email = ?, phone = ?, location = ?
#                 WHERE id = ?
#             """, (name, email, phone, location, user_id))
#             conn.commit()

#         flash('Profile updated successfully!', 'success')
#         return redirect(url_for('profile'))  # Redirect to the profile page

# def get_db_connection():
#     conn = sqlite3.connect('database.db', timeout=10)  # Timeout to avoid lock
#     conn.row_factory = sqlite3.Row
#     return conn

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         email = request.form['email']
#         role = request.form['role']
#         location = request.form['location']
#         contact = request.form['contact']

#         try:
#             with get_db_connection() as conn:
#                 cursor = conn.cursor()
#                 cursor.execute("""
#                     INSERT INTO users (username, password, email, role, location, contact)
#                     VALUES (?, ?, ?, ?, ?, ?)
#                 """, (username, password, email, role, location, contact))
#                 conn.commit()

#             flash('Registration successful! Please log in.', 'success')
#             return redirect(url_for('login'))
#         except sqlite3.OperationalError:
#             flash('Database is currently locked. Please try again later.', 'danger')
#             return redirect(url_for('register'))

#     return render_template('register.html')

# # @app.route("/login", methods=["GET", "POST"])
# # def login():
# #     if request.method == "POST":
# #         username = request.form.get("username")
# #         password = request.form.get("password")

# #         conn = sqlite3.connect("database.db")
# #         cursor = conn.cursor()
# #         cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
# #         user = cursor.fetchone()
# #         conn.close()

# #         if user:
# #             session["user_id"] = user[0]
# #             session["username"] = user[1]
# #             flash("Login successful!", "success")
# #             return redirect(url_for("start"))
# #         else:
# #             flash("Invalid username or password.", "danger")

# #     return render_template("login.html")

# # @app.route('/login', methods=['GET', 'POST'])
# # def login():
# #     if request.method == 'POST':
# #         username = request.form['username']
# #         password = request.form['password']

# #         with get_db_connection() as conn:
# #             cursor = conn.cursor()
# #             cursor.execute("""
# #                 SELECT * FROM users WHERE username = ? AND password = ?
# #             """, (username, password))
# #             user = cursor.fetchone()

# #             if user:
# #                 role = user['role']  # Get the user's role
# #                 if role == 'Customer':
# #                     flash('Login successful! Welcome back, Customer.', 'success')
# #                     return redirect(url_for('start'))  # Redirect to customer dashboard
# #                 elif role == 'Agent':
# #                     flash('Login successful! Welcome back, Agent.', 'success')
# #                     return redirect(url_for('delivery'))  # Redirect to agent dashboard
# #                 elif role == 'Admin':
# #                     flash('Login successful! Welcome back, Admin.', 'success')
# #                     return redirect(url_for('admin'))  # Redirect to admin dashboard
# #             else:
# #                 flash('Invalid username or password. Please try again.', 'danger')

# #     return render_template('login.html')

# @app.route('/submit_contact',methods=['GET','POST'])
# def submit_contact():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         message = request.form['message']
#         if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
#             flash("Invalid email format.", "error")
#             return redirect(url_for('register'))
#         print(name,email,message,sep='\n')
#     return redirect(url_for('start'))

# if __name__ == '__main__':
#     # init_db()
#     app.run(debug=True)

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
    #Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            location TEXT,
            contact TEXT,
            approved INTEGER NOT NULL DEFAULT 0  -- 0 = pending, 1 = approved, -1 = rejected
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
init_db()

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
            print(user)

            if user:
                session['user_id'] = user[0]
                session['username'] = user[1]
                session['email'] = user[2]
                session['role'] = user[4]
                session['location'] = user[5]
                session['contact'] = user[6]
                if username == "admin" and password == "123456":
                    flash('Login successful! Welcome back, Admin.', 'success')
                    return redirect(url_for('admin'))  # Redirect to admin dashboard
                else:
                    role = user['role']  # Get the user's role
                    if role == 'Customer':
                        # if user[7] == 0:
                        #     flash('Your account is pending approval.', 'warning')
                        #     return redirect(url_for('login'))
                        # elif user[7] == -1:
                        #     flash('Your account has been rejected.', 'danger')
                        #     return redirect(url_for('login'))
                        # else:
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
    return render_template('deliveryagent.html')

@app.route('/recovery')
def recovery():
    return render_template('recovery.html')

@app.route('/update_details', methods=['GET', 'POST'])
def update_details():
    if 'user_id' not in session:
        flash('Please log in to update your details.', 'danger')
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        new_username = request.form['username']
        new_email = request.form['email']
        new_role = request.form['role']
        new_location = request.form['location']
        new_contact = request.form['contact']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE users
                SET username = ?, email = ?, role = ?, location = ?, contact = ?
                WHERE id = ?
            ''', (new_username, new_email, new_role, new_location, new_contact, user_id))
            conn.commit()
            flash('Details updated successfully!', 'success')

            # Update session values
            session['username'] = new_username
            session['email'] = new_email
            session['role'] = new_role
            session['location'] = new_location
            session['contact'] = new_contact

            return redirect(url_for('start'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists. Please choose another.', 'danger')
        finally:
            conn.close()

    # Fetch current user details for the form
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, email, role, location, contact FROM users WHERE id = ?', (user_id,))
    user_details = cursor.fetchone()
    conn.close()

    return render_template('profile.html', user={
        'username': user_details[0],
        'email': user_details[1],
        'role': user_details[2],
        'location': user_details[3],
        'contact': user_details[4]
    })




@app.route('/viewprofile')
def viewprofile():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'danger')
        return redirect(url_for('login'))

    user_details = {
        'username': session.get('username'),
        'email': session.get('email'),
        'role': session.get('role'),
        'location': session.get('location'),
        'contact': session.get('contact'),
    }

    return render_template('viewprofile.html', user=user_details)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))

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

@app.route('/admin/approvals', methods=['GET'])
def admin_approvals():
    if 'user_id' not in session or session['role'] != 'admin':
        flash('Access restricted to administrators.', 'danger')
        return redirect(url_for('login'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email, role, contact FROM users WHERE approved = 0')
    pending_users = cursor.fetchall()
    conn.close()

    return render_template('approvals.html', pending_users=pending_users)

@app.route('/admin/approve_user/<int:user_id>', methods=['POST'])
def approve_user(user_id):
    if 'user_id' not in session or session['role'] != 'admin':
        flash('Access restricted to administrators.', 'danger')
        return redirect(url_for('login'))

    action = request.form['action']  # 'approve' or 'reject'
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if action == 'approve':
        cursor.execute('UPDATE users SET approved = 1 WHERE id = ?', (user_id,))
        flash('User approved successfully.', 'success')
    elif action == 'reject':
        cursor.execute('UPDATE users SET approved = -1 WHERE id = ?', (user_id,))
        flash('User rejected successfully.', 'danger')
    conn.commit()
    conn.close()

    return redirect(url_for('admin_approvals'))

# @app.route('/submit_profile', methods=['GET', 'POST'])
# def submit_profile():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         phone = request.form['phone']
#         location = request.form['location']
#         print(name,email,phone,location,sep='\n')
#         return redirect(url_for('start'))

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()  #create tables if they don't exists
    app.run(debug=True)