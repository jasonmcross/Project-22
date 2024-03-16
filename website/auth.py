from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for, session
from neon_python.userDB import DatabaseOperations

auth = Blueprint('auth', __name__)

db = DatabaseOperations()

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if len(email) < 8 or len(email) > 100 or len(password) < 8 or len(password) > 100:
            flash('Invalid email or password. Please try again.', category='error')
        else:
            # Lookup user in the database
            user_data = db.lookup_user(email)

            if user_data and user_data[0] == password:
                session['logged_in'] = True
                flash('Login successful!', category='success')
                return render_template("admin-home.html")

            else:
                flash('Invalid email or password. Please try again.', category='error')

    return render_template("admin-login.html")

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if 'logged_in' not in session:
        flash('Cannot view page', category='error')
        return render_template("admin-login.html")
    else:
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            con_password = request.form.get('con_password')
            name = request.form.get('name')
        
            if len(email) < 8 or len(email) > 100 or len(password) < 8 or len(password) > 100 or password != con_password:
                flash('Invalid input. Please try again.', category='error')
            else:
                # Add the new admin account to the database
                db.add_user(email, name, password)
                flash('Admin account created successfully.', category='success')
                session['logged_in'] = True
                return render_template("admin-home.html")
    
        return render_template("admin-sign-up.html")

@auth.route('/logout')
def logout():
    if 'logged_in' not in session:
        flash('Cannot view page', category='error')
        return render_template("admin-login.html")
    else:
        session.pop('logged_in', None)
        flash('Logged out sucessfully!', category='success')
        return render_template("developer-home.html")
