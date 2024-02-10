# from flask import Flask, Blueprint, render_template, request, flash

# auth = Blueprint('auth', __name__)


# @auth.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
        
#     return render_template("admin-login.html")

# @auth.route('/sign-up', methods=['GET', 'POST'])
# def sign_up():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
#         con_password = request.form.get('con_password')
        
#         if len(email) < 12:
#             flash('Invalid email entered.', category='error')
#         elif len(password) < 10:
#             flash('Invalid password length entered.', category='error')
#         elif password != con_password:
#             flash('Entered passwords do not match', category='error')
#         else:
#             flash('Admin account created successfully.', category='success')
        
#     return render_template("admin-sign-up.html")

# @auth.route('/logout')
# def logout():
#     return "<h1> Logout </h1>"




from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for
#from neon_python.userDB import DatabaseOperations


import os
import psycopg2
from dotenv import load_dotenv
auth = Blueprint('auth', __name__)


class DatabaseOperations:
    def __init__(self):
        load_dotenv()
        self.connection_string = "postgresql://PhilopateerAz:CF3q1wNWbOle@ep-lively-hat-a5tacpqp.us-east-2.aws.neon.tech/Project22?sslmode=require"
        print("url:", self.connection_string)
        self.conn = psycopg2.connect(self.connection_string)

    def __del__(self):
     if hasattr(self, 'conn') and self.conn is not None:
        self.conn.close()


    def add_user(self, email, name, password):
        cur = self.conn.cursor()
        sql = "INSERT INTO users (email, name, password) VALUES (%s, %s, %s)"
        cur.execute(sql, (email, name, password))
        self.conn.commit()
        cur.close()

    def remove_user(self, email):
        cur = self.conn.cursor()
        sql = "DELETE FROM users WHERE email = %s"
        cur.execute(sql, (email,))
        self.conn.commit()
        cur.close()

    def edit_user_password(self, email, new_password):
        cur = self.conn.cursor()
        sql = "UPDATE users SET password = %s WHERE email = %s"
        cur.execute(sql, (new_password, email))
        self.conn.commit()
        cur.close()

    def lookup_user(self, email):
        cur = self.conn.cursor()
        sql = "SELECT password FROM users WHERE email = %s"
        cur.execute(sql, (email,))
        result = cur.fetchone()
        cur.close()
        return result



db = DatabaseOperations()

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Lookup user in the database
        user_data = db.lookup_user(email)

        if user_data and user_data[0] == password:
            flash('Login successful!', category='success')
            return redirect(url_for('auth.logout'))
        else:
            flash('Invalid email or password. Please try again.', category='error')

    return render_template("admin-login.html")

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        con_password = request.form.get('con_password')
        
        if len(email) < 12:
            flash('Invalid email entered.', category='error')
        elif len(password) < 10:
            flash('Invalid password length entered.', category='error')
        elif password != con_password:
            flash('Entered passwords do not match', category='error')
        else:
            # Add the new admin account to the database
            db.add_user(email, 'Admin', password)
            flash('Admin account created successfully.', category='success')
            return redirect(url_for('auth.login'))
        
    return render_template("admin-sign-up.html")

@auth.route('/logout')
def logout():
    # return "<h1> Logout </h1>"
    return render_template("admin-home.html")
