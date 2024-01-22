from flask import Flask, Blueprint, render_template, request, flash
from website import predicttest

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def developer_home():
    if request.method == 'POST':
        problem = request.form.get('problem')
        collection = request.form.get('collection')
        
        if len(problem) < 2:
            flash('Enter a valid design problem.', category='error')
        else:
            patterns = predicttest.predictIt(problem)
            flash('Design problem submitted.', category='success')
            return render_template("developer-home.html", patterns=patterns)
        
    return render_template("developer-home.html")

@views.route('/admin-home', methods=['GET', 'POST'])
def admin_home():
    return render_template("admin-home.html")
