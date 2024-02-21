from flask import Flask, Blueprint, render_template, request, flash
from website import predicttest

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def developer_home():
    if request.method == 'POST':
        problem = request.form.get('problem')
        collection = request.form.get('collection')

        # Machine learning values
        vector = request.form.get('vector')
        cluster = request.form.get('cluster')
        
        test = request.form.get('flexCheck')

        print(test)
        
        if len(problem) < 2:
            flash('Enter a valid design problem.', category='error')
        elif len(problem) > 1000:
            flash('Enter a valid design problem.', category='error')
        elif collection == "0":
            flash('Select a digital library collection', category='error')
        else:
            patterns = predicttest.predictIt(problem, collection)
            flash('Design problem submitted.', category='success')
            return render_template("developer-home.html", patterns=patterns)
        
    return render_template("developer-home.html")

@views.route('/admin-home', methods=['GET', 'POST'])
def admin_home():
    if request.method =='POST':
        req = request.form.get('req')
        
        if req == "update":
            return render_template("admin-home.html")
        elif req == "delete":
            return render_template("admin-home.html")

    libraries = ["SourceMaking (Gang of Four)", "RefactoringGuru (Gang of Four)", "GeeksForGeeks (Gang of Four)"]
    return render_template("admin-home.html", libraries=libraries)
