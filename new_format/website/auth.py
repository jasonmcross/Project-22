from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for
from neon_python.userDB import DatabaseOperations

auth = Blueprint('auth', __name__)

db = DatabaseOperations()

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if len(email) < 12:
            flash('Invalid email entered.', category='error')
        elif len(email) > 100:
            flash('Invalid email entered.', category='error')
        elif len(password) < 10:
            flash('Invalid password length entered.', category='error')
        elif len(password) > 100:
            flash('Invalid password length entered.', category='error')
        else:
            # Lookup user in the database
            user_data = db.lookup_user(email)

            if user_data and user_data[0] == password:
                flash('Login successful!', category='success')
                libraries = ["SourceMaking (Gang of Four)", "RefactoringGuru (Gang of Four)", "GeeksForGeeks (Gang of Four)"]
                return render_template("admin-home.html", libraries=libraries)
            else:
                flash('Invalid email or password. Please try again.', category='error')

    return render_template("admin-login.html")

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        con_password = request.form.get('con_password')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        name = firstName + " " + lastName
        
        if len(email) < 12:
            flash('Invalid email entered.', category='error')
        elif len(email) > 100:
            flash('Invalid email entered.', category='error')
        elif len(password) < 10:
            flash('Invalid password length entered.', category='error')
        elif len(password) > 100:
            flash('Invalid password length entered.', category='error')
        elif password != con_password:
            flash('Entered passwords do not match', category='error')
        else:
            # Add the new admin account to the database
            db.add_user(email, name, password)
            flash('Admin account created successfully.', category='success')
            libraries = ["SourceMaking (Gang of Four)", "RefactoringGuru (Gang of Four)", "GeeksForGeeks (Gang of Four)"]
            return render_template("admin-home.html", libraries=libraries)
        
    return render_template("admin-sign-up.html")
  
@auth.route('/logout')
def logout():
    return render_template("developer-home.html")

