from flask import Flask, Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
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
            flash('Admin account created successfully.', category='success')
        
    return render_template("admin-sign-up.html")

@auth.route('/logout')
def logout():
    return "<h1> Logout </h1>"